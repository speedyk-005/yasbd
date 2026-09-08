import regex as re

from yasbd.rules.base import Rules
from yasbd.utils.trie import build_optimized_pattern


# fmt: off
class EsRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "sr", "sra", "srta", "d", "dña", "dra", "lic", "gral",
        "pdte", "profe", "profa", "arq", "abg", "cnel",
        "mag", "lcdo",

        # Military / Religious
        "cap", "cmdte", "tte", "subtte",
        "hno", "hnos", "pbro",

        # Noble / Royal
        "s.m", "ss.mm", "s.a.r", "ss.aa.rr", "s.a.s", "s.s", "s.a",
        "ss.aa", "s.e", "v.e", "s.à.s.r", "aa", "mm", "rr", "ss",
    }

    REFERENCE_ABBRVS = (Rules.REFERENCE_ABBRVS - {"no", "nos", "para"}) | {
        "pág", "núm", "nro", "dir", "t", "trad", "asoc", "aprox",
        "cf", "incl", "cía", "s",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Artículo", "Anexo", "Capítulo", "Sección", "Subsección", "Unidad",
        "Módulo", "División",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS - {"ave"} | {
        "ej", "p.ej", "vid", "cll", "cra", "diag", "transv", "mz", "mza", "lt",
        "urb", "asent", "dpto", "prov", "mnpio", "conj", "edif", "ofic", "km",
        "av", "avd", "c", "pso", "ctra", "pl", "blvr",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "EE.UU", "FF.AA", "RR.HH", "CC.AA", "EE", "UU", "FF", "RR", "HH", "AA",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "ene", "abr", "may", "ago", "dic", "lun" , "mar" ,"mié", "miér",
        "jue", "vie", "sáb", "dom",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas",

        # Pronouns
        "Allí", "Aquel", "Aquella", "Aquellas", "Aquellos",
        "Aquí", "Cual", "Cuales", "Cuanto", "Ella", "Ellas",
        "Ellos", "Esa", "Esas", "Ese", "Esos", "Esta", "Estas",
        "Este", "Estos", "Nosotros", "Quien", "Quienes", "Tú",
        "Usted", "Vosotros", "Yo", "Él",

        # Inverted punctuation (always start a new sentence in Spanish)
        "¿", "¡",

        # Adverbs & Transitions
        "Actualmente", "Además", "Afortunadamente", "Ahora",
        "Anoche", "Anteriormente", "Antes", "Antiguamente",
        "Así que", "Aunque", "Ayer", "Aún", "Casi",
        "Consecuentemente", "Después", "Entonces", "Finalmente",
        "Generalmente", "Hoy", "Incluso", "Inmediatamente",
        "Jamás", "Lamentablemente", "Luego", "Mañana", "Mejor",
        "Menos", "Mientras", "Más", "Normalmente", "Nunca",
        "Ojalá", "Peor", "Pero", "Posteriormente",
        "Previamente", "Primero", "Probablemente", "Pronto",
        "Próximamente", "Quizá", "Quizás", "Realmente",
        "Segundo", "Seguramente", "Siempre", "Simultáneamente",
        "Sin embargo", "Solamente", "Solo", "Subsiguientemente",
        "Sucesivamente", "Tal vez", "También", "Tampoco",
        "Tarde", "Temprano", "Tercero", "Todavía", "Ya",
        "Últimamente", "Último",

        # Question words
        "Como", "Cuando", "Cuál", "Cuándo", "Cuánto", "Cómo",
        "Donde", "Dónde", "Porque", "Porqué", "Quién", "Qué",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix pronouns abbrvs behavior."""
        super()._compile_regex_dynamically()


        # Ud./Uds./Vd./Vds. heuristic
        # Don't split if the next word is NOT a common starter (assumes it's a proper name).
        # Resolves the ambiguity "Ud. Marco" vs "Ud. Mañana".
        cls.MID_SENTENCE_FINDER_LST.append(
            re.compile(rf"""
                \b(?i:{build_optimized_pattern({"ud", "uds", "vd", "vds"})})\.
                (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
            """, re.X)
        )
