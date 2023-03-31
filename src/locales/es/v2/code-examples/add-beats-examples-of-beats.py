# Ejemplos de ritmos: Cómo crear ritmos en géneros diferentes

# Configuración
from earsketch import *
setTempo(120)

# Clips de sonido
bombo = OS_KICK05  # Este es el sonido "pum".
redoblante = OS_SNARE01  # Este es el sonido "cat".
hihat = OS_CLOSEDHAT01  # Este es el sonido "ts".

# Ritmo de rock en compás 1
makeBeat(bombo, 1, 1, "0+++----0+++----")
makeBeat(redoblante, 2, 1, "----0+++----0+++")
makeBeat(hihat, 3, 1, "0+0+0+0+0+0+0+0+")

# Ritmo de hip hop en compás 3
makeBeat(bombo, 1, 3, "0+++------0+++--")
makeBeat(redoblante, 2, 3, "----0++0+0++0+++")
makeBeat(hihat, 3, 3, "0+0+0+0+0+0+0+0+")

# Ritmo de jazz en compás 5
makeBeat(hihat, 3, 5, "0++0+00++0+0")

# Ritmo de dembow (latino, caribeño) en compás 7
makeBeat(bombo, 1, 7, "0+++0+++0+++0+++")
makeBeat(redoblante, 2, 7, "---0++0+---0++0+")