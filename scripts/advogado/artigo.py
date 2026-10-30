#!/usr/bin/env python3
"""Extrai artigos, súmulas e temas do acervo para o agente /advogado.

Uso:
  artigo.py <codigo> <art> [<art> ...]     artigo(s) de um código pelo apelido
  artigo.py <arquivo.md> <art> [...]       artigo(s) de qualquer norma do acervo
  artigo.py <codigo> --grep <termo>        linhas do código que citam o termo
  artigo.py sv|stf|stj|tst|tnu <n>         súmula (vinculante, STF, STJ, TST, TNU)
  artigo.py tema-stf|tema-stj <n>          tema de repercussão geral / repetitivo
  artigo.py --lista                        apelidos disponíveis

Exemplos: artigo.py cp 154-A 171   artigo.py cf 5   artigo.py cdc --grep "vício"
"""
import re
import signal
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
F = "federal/leis-ordinarias"

CODIGOS = {
    "cf": ("constituicao.md", "Constituição Federal de 1988"),
    "cp": ("federal/decretos-lei/1940/del-2848-1940-12-07.md", "Código Penal"),
    "cpp": ("federal/decretos-lei/1941/del-3689-1941-10-03.md", "Código de Processo Penal"),
    "lcp": ("federal/decretos-lei/1941/del-3688-1941-10-03.md", "Lei das Contravenções Penais"),
    "lindb": ("federal/decretos-lei/1942/del-4657-1942-09-04.md", "LINDB"),
    "clt": ("federal/decretos-lei/1943/del-5452-1943-05-01.md", "CLT"),
    "cc": (f"{F}/2002/lei-10406-2002-01-10.md", "Código Civil"),
    "cpc": (f"{F}/2015/lei-13105-2015-03-16.md", "Código de Processo Civil"),
    "cdc": (f"{F}/1990/lei-8078-1990-09-11.md", "Código de Defesa do Consumidor"),
    "eca": (f"{F}/1990/lei-8069-1990-07-13.md", "Estatuto da Criança e do Adolescente"),
    "ctn": (f"{F}/1966/lei-5172-1966-10-25.md", "Código Tributário Nacional"),
    "ctb": (f"{F}/1997/lei-9503-1997-09-23.md", "Código de Trânsito Brasileiro"),
    "jecrim": (f"{F}/1995/lei-9099-1995-09-26.md", "Juizados Especiais (Lei 9.099/95)"),
    "jef": (f"{F}/2001/lei-10259-2001-07-12.md", "Juizados Especiais Federais"),
    "jefp": (f"{F}/2009/lei-12153-2009-12-22.md", "Juizados da Fazenda Pública"),
    "marco-civil": (f"{F}/2014/lei-12965-2014-04-23.md", "Marco Civil da Internet"),
    "lgpd": (f"{F}/2018/lei-13709-2018-08-14.md", "LGPD"),
    "carolina-dieckmann": (f"{F}/2012/lei-12737-2012-11-30.md", "Lei 12.737/2012 (delitos informáticos)"),
    "fraude-eletronica": (f"{F}/2021/lei-14155-2021-05-27.md", "Lei 14.155/2021 (fraude eletrônica)"),
    "maria-da-penha": (f"{F}/2006/lei-11340-2006-08-07.md", "Lei Maria da Penha"),
    "drogas": (f"{F}/2006/lei-11343-2006-08-23.md", "Lei de Drogas"),
    "lep": (f"{F}/1984/lei-7210-1984-07-11.md", "Lei de Execução Penal"),
    "hediondos": (f"{F}/1990/lei-8072-1990-07-25.md", "Lei de Crimes Hediondos"),
    "interceptacao": (f"{F}/1996/lei-9296-1996-07-24.md", "Lei de Interceptação Telefônica"),
    "orcrim": (f"{F}/2013/lei-12850-2013-08-02.md", "Lei de Organizações Criminosas"),
    "abuso-autoridade": (f"{F}/2019/lei-13869-2019-09-05.md", "Lei de Abuso de Autoridade"),
    "anticrime": (f"{F}/2019/lei-13964-2019-12-24.md", "Pacote Anticrime"),
    "lavagem": (f"{F}/1998/lei-9613-1998-03-03.md", "Lei de Lavagem de Dinheiro"),
    "armas": (f"{F}/2003/lei-10826-2003-12-22.md", "Estatuto do Desarmamento"),
    "racismo": (f"{F}/1989/lei-7716-1989-01-05.md", "Lei do Racismo"),
    "ambiental": (f"{F}/1998/lei-9605-1998-02-12.md", "Lei de Crimes Ambientais"),
    "direito-autoral": (f"{F}/1998/lei-9610-1998-02-19.md", "Lei de Direitos Autorais"),
    "software": (f"{F}/1998/lei-9609-1998-02-19.md", "Lei do Software"),
    "propriedade-industrial": (f"{F}/1996/lei-9279-1996-05-14.md", "Lei de Propriedade Industrial"),
    "inquilinato": (f"{F}/1991/lei-8245-1991-10-18.md", "Lei do Inquilinato"),
    "alimentos": (f"{F}/1968/lei-5478-1968-07-25.md", "Lei de Alimentos"),
    "divorcio": (f"{F}/1977/lei-6515-1977-12-26.md", "Lei do Divórcio"),
    "idoso": (f"{F}/2003/lei-10741-2003-10-01.md", "Estatuto da Pessoa Idosa"),
    "pcd": (f"{F}/2015/lei-13146-2015-07-06.md", "Estatuto da Pessoa com Deficiência"),
    "gratuidade": (f"{F}/1950/lei-1060-1950-02-05.md", "Lei de Assistência Judiciária"),
    "mandado-seguranca": (f"{F}/2009/lei-12016-2009-08-07.md", "Lei do Mandado de Segurança"),
    "acp": (f"{F}/1985/lei-7347-1985-07-24.md", "Lei da Ação Civil Pública"),
    "arbitragem": (f"{F}/1996/lei-9307-1996-09-23.md", "Lei de Arbitragem"),
    "mediacao": (f"{F}/2015/lei-13140-2015-06-26.md", "Lei de Mediação"),
    "processo-adm": (f"{F}/1999/lei-9784-1999-01-29.md", "Processo Administrativo Federal"),
    "servidor": (f"{F}/1990/lei-8112-1990-12-11.md", "Estatuto do Servidor Federal"),
    "improbidade": (f"{F}/1992/lei-8429-1992-06-02.md", "Lei de Improbidade"),
    "anticorrupcao": (f"{F}/2013/lei-12846-2013-08-01.md", "Lei Anticorrupção"),
    "lai": (f"{F}/2011/lei-12527-2011-11-18.md", "Lei de Acesso à Informação"),
    "licitacoes": (f"{F}/2021/lei-14133-2021-04-01.md", "Lei de Licitações"),
    "oab": (f"{F}/1994/lei-8906-1994-07-04.md", "Estatuto da Advocacia"),
    "falencia": (f"{F}/2005/lei-11101-2005-02-09.md", "Lei de Falências e Recuperação"),
    "sa": (f"{F}/1976/lei-6404-1976-12-15.md", "Lei das S.A."),
    "liberdade-economica": (f"{F}/2019/lei-13874-2019-09-20.md", "Lei da Liberdade Econômica"),
    "simples": ("federal/leis-complementares/2006/lcp-123-2006-12-14.md", "Simples Nacional / ME-EPP"),
    "sigilo-bancario": ("federal/leis-complementares/2001/lcp-105-2001-01-10.md", "Sigilo Bancário"),
    "beneficios-inss": (f"{F}/1991/lei-8213-1991-07-24.md", "Planos de Benefícios da Previdência"),
    "custeio-inss": (f"{F}/1991/lei-8212-1991-07-24.md", "Custeio da Seguridade Social"),
    "loas": (f"{F}/1993/lei-8742-1993-12-07.md", "LOAS"),
    "eleitoral": (f"{F}/1965/lei-4737-1965-07-15.md", "Código Eleitoral"),
    "cade": (f"{F}/2011/lei-12529-2011-11-30.md", "Defesa da Concorrência"),
    "inovacao": (f"{F}/2004/lei-10973-2004-12-02.md", "Lei de Inovação"),
    "reforma-trabalhista": (f"{F}/2017/lei-13467-2017-07-13.md", "Reforma Trabalhista"),
}

JURIS = {
    "sv": ("jurisprudencia/stf/sumulas-vinculantes", "sumula-vinculante-{n}.md"),
    "stf": ("jurisprudencia/stf/sumulas", "sumula-{n}.md"),
    "stj": ("jurisprudencia/stj/sumulas", "sumula-{n}.md"),
    "tst": ("jurisprudencia/tst", "sumula-{n}.md"),
    "tnu": ("jurisprudencia/tnu/sumulas", "sumula-{n}.md"),
    "tema-stf": ("jurisprudencia/stf/repercussao-geral", "tema-{n}.md"),
    "tema-stj": ("jurisprudencia/stj/repetitivos", "tema-{n}.md"),
}

INICIO_ART = re.compile(r"^\*\*Art\.\s")


def cabecalho(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        return texto.split("\n", 1)[0].lstrip("# ")
    campos = {}
    for linha in m.group(1).splitlines():
        k, _, v = linha.partition(":")
        campos[k.strip()] = v.strip().strip('"')
    partes = [campos.get("titulo", "")]
    if campos.get("ementa"):
        partes.append(campos["ementa"])
    if campos.get("revogada") == "true":
        partes.append("⚠ REVOGADA")
    if campos.get("versao_texto"):
        partes.append(f"versão: {campos['versao_texto']}")
    if campos.get("fonte"):
        partes.append(f"fonte: {campos['fonte']}")
    return " | ".join(p for p in partes if p)


def padrao_artigo(num):
    num = num.strip().upper().replace("º", "").replace("°", "")
    base, _, sufixo = num.partition("-")
    base = base.replace(".", "")
    # milhar com ponto no texto: 1694 casa "1.694"
    grupos = []
    while len(base) > 3:
        grupos.insert(0, base[-3:])
        base = base[:-3]
    alvo = r"\.?".join([re.escape(base)] + grupos) + (r"[º°o]?-" + re.escape(sufixo) if sufixo else r"[º°o]?")
    # o número não pode continuar (121 ≠ 121-A, 12 ≠ 120)
    return re.compile(r"^\*\*Art\.\s*" + alvo + r"(?![\d\-]|-[A-Z])[\s.*]")


def extrair(caminho, artigos):
    texto = caminho.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    print(f"# {caminho.relative_to(RAIZ)}\n# {cabecalho(texto)}\n")
    for num in artigos:
        pad = padrao_artigo(num)
        achou = False
        for i, linha in enumerate(linhas):
            if not pad.match(linha):
                continue
            achou = True
            fim = i + 1
            while fim < len(linhas) and not INICIO_ART.match(linhas[fim]) and not linhas[fim].startswith("#"):
                fim += 1
            print(f"--- Art. {num} (linha {i + 1}) ---")
            print("\n".join(l for l in linhas[i:fim] if l.strip()))
            print()
        if not achou:
            print(f"--- Art. {num}: NÃO ENCONTRADO neste arquivo ---\n")


def grep(caminho, termo):
    texto = caminho.read_text(encoding="utf-8")
    print(f"# {caminho.relative_to(RAIZ)}\n# {cabecalho(texto)}\n")
    art_atual = "?"
    termo_l = termo.lower()
    n = 0
    for i, linha in enumerate(texto.splitlines(), 1):
        m = re.match(r"^\*\*Art\.\s*([\d.]+[º°o]?(?:-[A-Z]+)?)", linha)
        if m:
            art_atual = m.group(1)
        if termo_l in linha.lower():
            n += 1
            print(f"[Art. {art_atual} | linha {i}] {linha[:400]}")
            if n >= 60:
                print("... (truncado em 60 ocorrências)")
                return


def resolver(alvo):
    if alvo in CODIGOS:
        return RAIZ / CODIGOS[alvo][0]
    p = Path(alvo)
    if not p.is_absolute():
        p = RAIZ / p
    return p if p.exists() else None


def main(args):
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--lista":
        for k, (p, nome) in CODIGOS.items():
            print(f"{k:24} {nome:45} {p}")
        for k, (d, f) in JURIS.items():
            print(f"{k:24} {'(jurisprudência)':45} {d}/{f}")
        return 0
    alvo = args[0].lower()
    if alvo in JURIS:
        pasta, modelo = JURIS[alvo]
        for n in args[1:]:
            achados = list((RAIZ / pasta).rglob(modelo.format(n=n)))
            if not achados:
                print(f"--- {alvo} {n}: NÃO ENCONTRADA no acervo ---\n")
            for p in achados:
                print(f"# {p.relative_to(RAIZ)}")
                print(p.read_text(encoding="utf-8"))
        return 0
    caminho = resolver(args[0])
    if caminho is None:
        print(f"Apelido ou arquivo desconhecido: {args[0]} (use --lista)", file=sys.stderr)
        return 1
    if len(args) >= 3 and args[1] == "--grep":
        grep(caminho, " ".join(args[2:]))
    elif len(args) >= 2:
        extrair(caminho, args[1:])
    else:
        print(caminho.read_text(encoding="utf-8")[:4000])
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main(sys.argv[1:]))
