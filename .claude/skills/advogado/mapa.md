# Mapa do acervo para o /advogado

Apelidos entre `crases` funcionam em `python3 scripts/advogado/artigo.py <apelido> <art>`.
Os números de artigo abaixo são pontos de partida — **sempre extraia o texto antes de citar**.

## Garantias e base de qualquer defesa
- `cf` art. 5º (II legalidade, X intimidade, XII sigilo de comunicações, XXXV acesso à
  justiça, XXXIX anterioridade penal, XL retroatividade benéfica, LIV-LV devido processo e
  ampla defesa, LVI prova ilícita, LVII presunção de inocência, LXIII direito ao silêncio,
  LXVIII habeas corpus, LXIX mandado de segurança, LXXIV assistência jurídica gratuita).
- `lindb` arts. 1º-6º (vigência, irretroatividade), 20-30 (decisão administrativa).

## Penal / processo penal
- `cp`: 1º-4º (lei no tempo), 13-25 (dolo, culpa, erro, excludentes), 59-76 (pena e
  dosimetria), 107-119 (extinção da punibilidade e **prescrição**), 138-145 (honra),
  147 (ameaça), 147-A (perseguição/stalking), 154-A/154-B (invasão de dispositivo),
  155 (furto, §4º-B eletrônico), 171 (estelionato, §2º-A fraude eletrônica, §5º
  representação), 266 (interrupção de serviço telemático), 288 (associação criminosa),
  297-299 (falsidades), 313-A/313-B (sistemas da Administração).
- `cpp`: 3º-A a 3º-F (juiz das garantias), 5º-23 (inquérito), 28-A (ANPP), 155-157
  (prova, ilicitude e derivação), 158-A a 158-F (**cadeia de custódia** — prova digital),
  240-250 (busca e apreensão), 282-350 (prisões e cautelares), 396-397 (resposta à
  acusação e absolvição sumária), 564 (nulidades), 647-667 (habeas corpus).
- `jecrim` 61 (menor potencial ofensivo), 69, 72-76 (composição e transação), 89 (sursis
  processual). `lep`, `hediondos`, `anticrime`, `abuso-autoridade`, `interceptacao`,
  `orcrim`, `lavagem`, `drogas` (28 uso × 33 tráfico), `armas`, `maria-da-penha`, `racismo`,
  `ambiental`, `lcp` (contravenções).

## Cibernético / tech / segurança da informação
- `cp` 154-A ("sem autorização expressa ou tácita" — núcleo da defesa em pentest/bug
  bounty: escopo e autorização por escrito), 154-B (ação penal condicionada), 171 §2º-A,
  155 §4º-B, 266 §1º, 313-A.
- `carolina-dieckmann` (Lei 12.737/2012), `fraude-eletronica` (Lei 14.155/2021).
- `marco-civil` arts. 7º (direitos do usuário), 10-17 (guarda de registros), 18-21
  (responsabilidade de provedores; 19 ordem judicial; 21 nudez não consentida), 22
  (requisição judicial de registros).
- `lgpd` arts. 6º-7º, 11, 18 (direitos do titular), 42-45 (responsabilidade), 46-49
  (segurança e **incidentes** — art. 48), 52 (sanções ANPD).
- `software`, `direito-autoral` (art. 46 limitações), `propriedade-industrial` (195 —
  concorrência desleal/segredo industrial).
- Normas da ANPD/ANATEL/BCB: `scripts/advogado/buscar.sh ementa "<termo>" reguladores`.
- Observação: o Brasil **não tem** safe harbor legal específico para pesquisa de
  vulnerabilidade (até a data do acervo — confirme com `buscar.sh texto`). A defesa
  depende de autorização (contrato, termo do programa de bug bounty), ausência de dolo e
  ausência de dano.

## Civil / consumidor / família
- `cc`: 104-184 (negócio jurídico, defeitos), 186-188 e 927-954 (**responsabilidade civil**
  e dano moral), 189-211 (prescrição/decadência — 205 e 206), 389-420 (inadimplemento,
  juros, cláusula penal), 421-480 (contratos), 1.694-1.710 (alimentos).
- `cdc`: 6º (direitos básicos, VIII inversão do ônus), 12-14 (fato do produto/serviço),
  18-20 (vício), 26-27 (prazos), 35, 39 (práticas abusivas), 42 par. único (repetição em
  dobro), 43 (cadastros/negativação), 49 (arrependimento em 7 dias), 51 (cláusulas abusivas).
- `inquilinato`, `alimentos`, `divorcio`, `eca`, `idoso`, `pcd`.
- `cpc`: 98-102 (gratuidade), 219 e 231 (contagem de prazos), 300-311 (tutela de
  urgência/evidência), 335-342 (contestação), 373 (ônus da prova), 485-487, 1.003-1.044
  (recursos; 1.003 §5º prazo de 15 dias). `jecrim` 3º, 9º (JEC sem advogado até 20 SM).
  `jef`, `jefp`, `mandado-seguranca`, `acp`, `arbitragem`, `mediacao`, `gratuidade`.

## Trabalho e previdência
- `clt` (atenção: o arquivo tem o decreto-lei e a CLT — o script mostra as duas
  numerações; use a do corpo da Consolidação): 2º-3º (vínculo), 58-75 (jornada),
  442-B (autônomo), 477-486 (rescisão, 482 justa causa, 483 rescisão indireta), 611-A,
  791-A (honorários), 818 (ônus da prova), 840-841.
- Súmulas `tst`. `beneficios-inss`, `custeio-inss`, `loas`, súmulas `tnu`.

## Tributário / empresarial / administrativo
- `ctn` 3º, 97, 113-118, 142-150, 151 (suspensão), 156, 168, 173-174 (decadência e
  prescrição), 174, 185. `simples`, `sigilo-bancario`, `sa`, `falencia`,
  `liberdade-economica`, `cade`, `inovacao`.
- `processo-adm`, `servidor`, `improbidade`, `anticorrupcao`, `lai`, `licitacoes`, `oab`.
- Normas da RFB/PGFN/CARF/CVM/BCB: `buscar.sh ementa "<termo>" reguladores`.

## Trânsito
- `ctb` 161-255 (infrações), 256-268 (penalidades), 280-290 (processo administrativo,
  defesa prévia e recursos JARI/CETRAN), 291-312-B (crimes, 306 embriaguez, 302-303
  homicídio/lesão culposa). Resoluções do CONTRAN: `buscar.sh ementa "<termo>" reguladores`.

## Estadual e municipal
- `buscar.sh uf <UF> "<termo>"` — leis estaduais (IPVA, ICMS, taxas, servidores estaduais).
- `buscar.sh mun <UF> "<termo>"` — leis municipais disponíveis (ISS, IPTU, posturas, barulho).
  A cobertura municipal é parcial: veja `COBERTURA.md`.

## Jurisprudência (pastas)
- `jurisprudencia/stf/{sumulas-vinculantes,sumulas,repercussao-geral,controle-concentrado}`
- `jurisprudencia/stj/{sumulas,repetitivos}` · `jurisprudencia/tst` · `jurisprudencia/tnu`
- `jurisprudencia/trf4` · `jurisprudencia/outros-tribunais/{stm,tcu}`
