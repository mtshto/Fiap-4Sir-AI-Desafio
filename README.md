# Desafio Visão Computacional - Analytics de Futebol usando Visão Computacional

## Desafio de Visão Computacional

### Disciplina: AI Engineering, Cognitive and Semantic Computation & IoT
### Professor: Arnaldo Alves Viana Júnior
### Grupo: 
- Matheus de Oliveira (RM: 88430)
- Vitor Torres Dantas (RM: 88415)
- Marcio Yukio Takarave (RM: 86662)
- Felipe Nunes Pereira Leite (RM: 88254)
- Gilberto Moreira Santos Junior (RM: 88682)

## Definição do Projeto

O objetivo do nosso projeto é desenvolver um Analytics de Futebol usando visão computacional. Este Analytics será gerado com base na análise de vídeos de partidas de futebol, identificando os jogadores. Além disso, o Analytics irá detectar informações como a de posse de bola, passe de bola, e o gol.

### Projeto Base

Para realizar este projeto, decidimos utilizar a biblioteca/lib Ultralytics - YOLO (You Only Look Once) devido à sua eficácia na detecção e identificação de objetos em vídeos. Como base para o desenvolvimento, estamos utilizando o projeto disponível em: [YOLOv8-football](https://github.com/noorkhokhar99/YOLOv8-football).

### Apresentação do Projeto

[Veja a apresentação de slides]<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vSLLEI-OCvqdW3naUhHPCXyoaWHCXePR8_ooOTGC6U2U79H7Fs66-1dz2HgRELVn-koupcMjH5Hd0LP/embed?start=false&loop=false&delayms=30000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

## Rubrica de Avaliação

### Critérios de Avaliação:

1. **Inovação e Criatividade na Abordagem do Problema:** (3 Pontos)
   - [ ] 3 - Abordagem bem implementada e com features diferentes das usuais.
   - [ ] 1,5 - Abordagem seguindo os projetos já existentes e sem diferencial.


2. **Eficiência e Precisão da Solução de Visão Computacional:** 4 (pontos)
   - [ ] 4 - Solução identificando todos os jogadores, e a bola.
   - [ ] 2 - Solução identificando os jogadores.

3. **Features:** (3 pontos)
   - [ ] 3 - Identificar quando for gol
   - [ ] 2 - Detectar passe de bola
   - [ ] 1 - Detectar posse de bola

### Como executar o projeto:

#### Importante ter instalado o Python, OpenCV, Numpy, Pytorch

- Clone o repositório:
```
git clone https://github.com/mtshto/Fiap-4Sir-AI-Desafio.git
```

- Acesse a pasta do projeto
```
cd Fiap-4Sir-AI-Desafio
```

- Install o pacote do ultralytics
```
pip3 install ultralytics
```

- Install o pacote do omegaconf
```
pip install omegaconf
```


- Acesse a pasta onde está o arquivo de execução .py
```
cd src
```

- Execute o projeto com
```
python3 football-analytics.py
```
