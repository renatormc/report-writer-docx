from doc_handler import DocxHandler

handler = DocxHandler("generico")
context = {
    'rg': 123,
    'ano': 2021,
    'seq': 123,
    'relator': 'João das Couves',
    'revisor': 'Fulano de Tal',
    'requisitante': 'Delegacia de Tóquio',
    'ocorrencia_odin': '123/2021',
    'inicio_exame': '12/12/2021',
    'data_odin': '12/12/2021',
    'autoridade': 'José Costa Pereira',
    'data_recebimento': '12/10/2021',
    'procedimento': 'RAI 123/2021'
}
handler.render(context, "test.docx")