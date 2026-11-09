import os
from flask import Flask, request, redirect, session, jsonify, render_template
import mysql.connector

app = Flask(__name__)
# Chave de segurança para gerenciar as sessões de login dos funcionários
app.secret_key = "totvs_salesforce_secret_token_multinational"

# -----------------------------------------------------------------
# CONEXÃO HÍBRIDA DINÂMICA (Aiven na Nuvem / Localhost Máquina)
# -----------------------------------------------------------------
def get_db():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'admin1234'),
        database=os.environ.get('MYSQL_DB', 'erp_quimico'),
        port=int(os.environ.get('MYSQL_PORT', 3306))
    )

# -----------------------------------------------------------------
# CONTROLE DE PERMISSÕES CORPORATIVAS (Simulador de Login)
# -----------------------------------------------------------------
@app.route('/auth/login/<cargo>')
def login_simulado(cargo):
    session['usuario'] = f"User_{cargo}"
    session['cargo'] = cargo.upper()
    return redirect('/')

@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect('/')

# -----------------------------------------------------------------
# DASHBOARD PRINCIPAL - FLUXO DARK NEON PROTEGIDO
# -----------------------------------------------------------------
@app.route('/')
def index():
    # FIX: Evita loop de redirecionamento que quebrava o Render (Erro 500)
    if 'cargo' not in session:
        session['usuario'] = "User_gerente"
        session['cargo'] = "GERENTE"

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # 1. Busca contagem de pendências por setor (Visão Gerencial por Hora)
    cur.execute("SELECT COUNT(*) as qtd FROM pedidos WHERE status = 'PEND_ADM'")
    p_adm = cur.fetchone()['qtd']
    
    cur.execute("SELECT COUNT(*) as qtd FROM pedidos WHERE status = 'PEND_FISCAL'")
    p_fiscal = cur.fetchone()['qtd']
    
    cur.execute("SELECT COUNT(*) as qtd FROM pedidos WHERE status = 'PEND_LOG'")
    p_log = cur.fetchone()['qtd']

    # 2. Busca o Estoque Real-time dos produtos químicos nos Silos
    cur.execute("SELECT id, nome, quantidade_estoque, formula_quimica FROM produtos")
    estoque = cur.fetchall()

    # 3. Busca a Carteira de Pedidos de Venda (Estilo CRM)
    cur.execute("SELECT id, vendedor, valor_total, status FROM pedidos ORDER BY id DESC")
    pedidos = cur.fetchall()

    cur.close()
    conn.close()

    # Renderiza o arquivo HTML final Preto com Azul Neon
    return render_template('dashboard.html', 
                           cargo=session['cargo'], 
                           usuario=session['usuario'], 
                           adm=p_adm, 
                           fiscal=p_fiscal, 
                           log=p_log, 
                           estoque=estoque, 
                           pedidos=pedidos)

# -----------------------------------------------------------------
# ÁREA FISCAL - EMISSÃO INTEGRADA DE NOTAS (IMPOSTOS MANUAIS)
# -----------------------------------------------------------------
@app.route('/faturamento/emitir/<int:pedido_id>', methods=['POST'])
def emitir_nota(pedido_id):
    # REQUISITO: Restrição de acesso para funcionários de outros setores menores
    if session.get('cargo') not in ['FISCAL', 'GERENTE']:
        return "Erro 403: Acesso negado. Seu setor não possui permissão de faturamento.", 403

    icms = float(request.form.get('icms', 0))
    ipi = float(request.form.get('ipi', 0))
    valor_total = float(request.form.get('valor_total', 0))

    # Cálculo dinâmico baseado nos insumos informados manualmente na hora pelo fiscal
    valor_impostos = valor_total * ((icms + ipi) / 100)
    valor_final = valor_total + valor_impostos

    conn = get_db()
    cur = conn.cursor()

    # FIX: Ajustado coluna 'valor_final' para 'valor_final_nota' para bater com o banco Aiven
    cur.execute("""
        INSERT INTO notas_fiscais (pedido_id, aliquota_icms, aliquota_ipi, valor_impostos, valor_final_nota, emitido_por)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (pedido_id, icms, ipi, valor_impostos, valor_final, session['usuario']))
    
    # Avança a fase do fluxo do pedido para a Logística de Carga
    cur.execute("UPDATE pedidos SET status = 'PEND_LOG' WHERE id = %s", (pedido_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# -----------------------------------------------------------------
# MÓDULO LOGÍSTICO - DESPACHO, PESAGEM E SEGURO DE CARGA
# -----------------------------------------------------------------
@app.route('/logistica/despachar/<int:pedido_id>', methods=['POST'])
def despachar_carga(pedido_id):
    # REQUISITO: Restrição para funcionários menores de outros setores
    if session.get('cargo') not in ['LOGISTICA', 'GERENTE']:
        return "Erro 403: Acesso restrito ao departamento de Logística.", 403

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # 1. Realiza a baixa automatizada do estoque em tempo real na saída do caminhão
    cur.execute("SELECT produto_id, quantidade_toneladas FROM pedidos WHERE id = %s", (pedido_id,))
    ped = cur.fetchone()
    
    if ped:
        cur.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque - %s WHERE id = %s", 
                    (ped['quantidade_toneladas'], ped['produto_id']))

    # 2. Registro e Auditoria completa da Frota e Carregamento Químico
    possui_seguro = 1 if 'seguro' in request.form else 0
    cur.execute("""
        INSERT INTO logistica_cargas (pedido_id, empresa_caminhao, placa, rota, peso_bruto_kg, tipo_carga, possui_seguro, data_hora_entrada, data_hora_saida)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
    """, (pedido_id, request.form.get('empresa'), request.form.get('placa'), request.form.get('rota'),
          request.form.get('peso'), request.form.get('tipo_carga'), possui_seguro))

    # 3. Finaliza a ordem de venda com status concluído
    cur.execute("UPDATE pedidos SET status = 'CONCLUIDO' WHERE id = %s", (pedido_id,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# -----------------------------------------------------------------
# REQUISITO DE INTEGRAÇÃO: SINCRONISMO COM OUTROS BANCOS DE DADOS
# -----------------------------------------------------------------
@app.route('/api/v1/sincronizar', methods=['POST'])
def integrar_sistemas_externos():
    # Rota API que permite que qualquer outro sistema externo atualize o estoque por hora via JSON
    dados = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    
    for item in dados.get('produtos', []):
        cur.execute("""
            UPDATE produtos SET quantidade_estoque = %s WHERE nome = %s
        """, (item['estoque'], item['nome']))
        
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "Success", "message": "Estoque integrado e sincronizado."})

if __name__ == '__main__':
    app.run(debug=True)
