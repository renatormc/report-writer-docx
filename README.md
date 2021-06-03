# Report Writer Docx

- Os modelos são definidos dentro da pasta models. 
- Cada subpasta será considerada um modelo distinto
- Dentro de cada pasta de modelo tem de haver uma pasta de nome "templates" na qual devem ser inseridos os arquivos docx de template.
- O arquivo template de nome Main.docx é o principal, os demais serão auxiliares para serem inseridos dentro do principal caso necessário
- Antes do contexto ser repassado para o template ele passa por um preprocessamento que pode ser definido dentro do arquivo pre.py que fica dentro da pasta do modelo
