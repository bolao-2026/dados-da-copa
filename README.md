# Copa 2026

Repositório de dados públicos e estáticos da Copa 2026.

Os dados de interesse, ficam armazenados no diretório `/dados`
(por ora, a tabela da copa e a lista de países).

## Atualização

Para atualizar os dados, basta rodar o `/bin/fetch-worldcup-json`
do diretório base do repo, esperar o processo terminar e, em
seguida, rodar o script `/bin/traduz-tabela.py`. Em seguida, faça
o commit dos dados atualizados.

O primeiro script faz um clone e checkout seletivo do repositório
com o conteúdo original e descarta tudo, deixando apenas os dados
de interesse. Como esses dados mudam pouco, minha expectativa é
que isso não mude, exceto se o autor achar algum erro. O segundo
script faz a tradução e adaptação da tabela fonte para a tabela
no formato necessário para o Bolão da Copa 2026.
