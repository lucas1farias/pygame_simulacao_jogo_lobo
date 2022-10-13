

# pygame_simulacao_jogo_lobo (Português)
<p>Simulacro de jogo em Pygame usando recursos importantes do biblioteca (superfícies, colisão, sprites animados, movimento de câmera)</p> 

<h4>Instalar dependências</h4>
<p>pip install -r dependencies.txt</p>

<h4>Detalhes</h4>
<ol>
  <li>Esse repositório é diretamente relacionado ao repositório <p>pygame_criar_mapas</p></li>
  <li>Ao executar um dos arquivos em <b>pygame_criar_mapas</b>, é gerado no terminal um array de strings e este array pode ser copiado e usado neste repositório em <b>config/settings.py</b></li>
  <li>Em <b>config/settings.py</b>, os mapas existentes foram criados via repositório <b>pygame_criar_mapas</b></li>
  <li>Em <b>config/settings.py</b>, apesar dos mapas serem aleatórios, é possível optar por criar manualmente</li>
  <li>Em <b>config/settings.py</b>, a variável <b>scenario2"</b> é um exemplo de um cenário customizado</li>
  <li>Em <b>config/settings.py</b>, cada array de strings contêm um "X", que representa uma superfície (escolha opcional do caracter)</li>
  <li>Em <b>config/settings.py</b>, cada array de strings não vêm com um jogador, este foi adicionado manualmente via <b>caracter P</b></li>
  <li>Para substituir mapas, ir ao módulo <b>objects/scenario.py</b>, procurar por <b>self.setup_level</b> e trocar o parâmetro por um novo array de strings ou outra variável vinda de <b>config/settings.py</b></li>
</ol>

<h4>Algoritmo</h4>
<p>launcher.py</p>

# pygame_simulacao_jogo_lobo (English)
<p>Simulacrum of a Pygame game using important resources from the library (surfaces, collision, animated sprites, camera motion)</p>

<h4>Install dependencies</h4>
<p>pip install -r dependencies.txt</p>

<h4>Details</h4>
<ol>
  <li>This repository is straighly related with the repository <p>pygame_criar_mapas</p></li>
  <li>After running files from <b>pygame_criar_mapas</b>, it is generated an array of strings on the terminal, which can be copied and used in this repository, in <b>config/settings.py</b></li>
  <li>In <b>config/settings.py</b>, existing maps were created by the repository <b>pygame_criar_mapas</b></li>
  <li>In <b>config/settings.py</b>, besides maps are random, they can be created manually</li>
  <li>In <b>config/settings.py</b>, the variable <b>scenario2"</b> is an example of a custom scenario</li>
  <li>In <b>config/settings.py</b>, each array of strings has an "X", which represents one surface (character picked is optional)</li>
  <li>In <b>config/settings.py</b>, each array of string do not come with a player, it was added manually by <b>the character P</b></li>
  <li>To replace maps, go to the module <b>objects/scenario.py</b>, and look for <b>self.setup_level</b>, change the parameter for a new array of strings or another variable from <b>config/settings.py</b></li>
</ol>

<h4>Algorithm</h4>
<p>launcher.py</p>
