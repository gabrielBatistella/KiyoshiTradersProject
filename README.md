# KiyoshiTradersProject
Trabalho do grupo Kiyoshi Traders para a disciplina de Sistemas Embarcados

<h1 align="center">:file_cabinet: Planejamento de Trajetórias para Barret-WAM (4DOF)</h1>

## :memo: Descrição
O projeto tem como finalidade fazer o planejamento de trajetória para o manipulador Barret-WAM, que possui 4 graus de liberdade.

O usuário poderá optar por uma trajetória linear ou curva, e a partir de pontos dados pelo usuário, o programa montará uma trajetória passando por esses, mostrando o gráfico do ângulo de cada junta do manipulador e em seguida a trajetória em 3D.

## :books: Interface com o usuário
* <b>Select manipulator</b>: Seleciona o atuador, por enquanto tem-se apenas (1), o Barret-WAM.
* <b>Select trajectory type</b>: Seleciona o tipo de trajetória, (1) para trajetória curvada e (2) para trajetória linear.
* <b>Enter the coordinates for point</b>: Insere os pontos da trajetória, são aceitos apenas pontos dentro do espaço de trabalho. O formato aceito para os pontos é com um <i>Space</i> entre as coordenadas, e um <i>Enter</i> entre um ponto e outro, por exemplo: 0.35 0 0.55. Após inserido os pontos, escrever F para sinalizar o fim dos pontos.

## :wrench: Tecnologias utilizadas
* Python;

## :rocket: Rodando o projeto
Para rodar o repositório é necessário clonar o mesmo e executar o seguinte comando para iniciar o programa:
```
python main.py
```

## :handshake: Colaboradores
<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/aurora-maciel-372222208/">
        <img src="https://media.licdn.com/dms/image/C5603AQGuvSTYPagPKw/profile-displayphoto-shrink_400_400/0/1627326652584?e=1677110400&v=beta&t=1sAlX4Nz6c-SX6QS1vuOJXHleZlt6zJxRYaTG0TyEPY" width="100px;" alt="Foto de Aurora Maciel no Linkedin"/><br>
        <sub>
          <b>Aurora Maciel</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/benitopma/">
        <img src="https://media.licdn.com/dms/image/C4E03AQEtmrCLSdFDbw/profile-displayphoto-shrink_400_400/0/1629163379456?e=1677110400&v=beta&t=k3Fn-oxai0QqApJc7m_a8zCdPieB3UYLJlFEMi3DdDM" width="100px;" alt="Foto de Benito Palma no Linkedin"/><br>
        <sub>
          <b>Benito Palma</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/gabriel-batistella-768a8a256/">
        <img src="https://media.licdn.com/dms/image/D4D03AQEzfBY82uXinw/profile-displayphoto-shrink_400_400/0/1671499115631?e=1677110400&v=beta&t=CRu6GbETipr99-rx7hJwWWGNYSxZ7EIc6bKEaUQvl_g" width="100px;" alt="Foto de Gabriel Batistella no Linkedin"/><br>
        <sub>
          <b>Gabriel Batistella</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/henrique-chen/">
        <img src="https://media.licdn.com/dms/image/C4E03AQExCTJa3-r6HQ/profile-displayphoto-shrink_400_400/0/1661945777329?e=1677110400&v=beta&t=vE-O7zzfaLD2YDugxeKrtJmiZj-PxJtj-9unyS6OD2g" width="100px;" alt="Foto de Henrique Chen no Linkedin"/><br>
        <sub>
          <b>Henrique Chen</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## :soon: Implementação futura
* Adicionar outros manipuladores (Já conta com biblioteca para tal)
* Adicionar outras formas de trajetórias, como circulares (Também conta com biblioteca para tal)
* Implementar simulação mostrando o manipulador todo realizando a trajetória
