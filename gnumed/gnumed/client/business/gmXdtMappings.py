# -*- encoding: utf8 -*-
"""GnuMed German XDT mapping data.

This maps XDT fields in various ways.
"""
#==============================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/business/gmXdtMappings.py,v $
# $Id: gmXdtMappings.py,v 1.41 2007-06-15 07:58:01 ncq Exp $
__version__ = "$Revision: 1.41 $"
__author__ = "S.Hilbert, K.Hilbert"
__license__ = "GPL"

try:
	_('dummy-no-need-to-translate-but-make-epydoc-happy')
except NameError:
	_ = lambda x:x

#==============================================================
xdt_id_map = {

	'6295': '??',
	'6296': '??',
	'6297': '??',
	'6298': '??',
	'6299': '??',

	'0101': 'KBV-Prüfnummer',
	'0102': 'Softwareverantwortlicher',
	'0103': 'Softwarename',
	'0104': 'Hardware',
	'0105': 'KBV-Prüfnummer',
	'0111': 'Email-Adresse des Softwareverantwortlichen',
	'0121': 'Strasse des Softwareverantwortlichen',
	'0122': 'PLZ des Softwareverantwortlichen',
	'0123': 'Ort des Softwareverantwortlichen',
	'0124': 'Telefonnummer des Softwareverantwortlichen',
	'0125': 'Telefaxnummer des Softwareverantwortlichen',
	'0126': 'Regionaler Systembetreuer',
	'0127': 'Strasse des Systembetreuers',
	'0128': 'PLZ des Systembetreuers',
	'0129': 'Ort des Systembetreuers',
	'0130': 'Telfonnummer des Systembetreuers',
	'0131': 'Telefaxnummer des Systembetreuers',
	'0132': 'Release-Stand der Software',

	'0201': 'Arztnummer',
	'0202': 'Praxistyp',		# 1=EP, 2=GP, 3=FachGP, 4=PG, 5=FaPG
	'0203': 'Arztname',
	'0204': 'Arztgruppe verbal',
	'0205': 'Strasse der Praxisadresse',
	'0206': 'PLZ Ort der Praxisadresse',
	'0207': 'Arzt mit Leistungskennzeichen',
	'0208': 'Telefonnummer der Praxis',
	'0209': 'Telefaxnummer der Praxis',
	'0210': 'Modemnummer der Praxis',
	'0211': 'Arztname für Leistungsdifferenzierung',
	'0213': 'Leistungskennzeichen',
	'0214': 'Erläuterung zum Leistungskennzeichen',
	'0215': 'PLZ der Praxisadresse',
	'0216': 'Ort der Praxisadresse',
	'0218': 'E-Mail der Praxis/des Arztes',
	'0225': 'Anzahl der Ärzte',

	'0250': 'Name erste freie Kategorie',
	'0251': 'Inhalt erste freie Kategorie',

	'0915': 'PZN Medikament auf Kassenrezept',
	'0917': 'Packungsgrösse Medikament auf Kassenrezept',
	'0918': 'Packungsgrösse Medikament auf Privatrezept',
	'0919': 'Hilfsmittelbezeichnung',
	'0920': 'Hilfsmittelnummer',
	'0922': 'PZN Hilfsmittel',
	'0923': 'Anzahl Hilfsmittel',
	'0925': 'Heilmittel',
	'0950': 'PZN Dauermedikament',
	'0951': 'PZN Medikament auf Privatrezept',
	'0952': 'PZN Ärztemuster',
	'0953': 'Packungsgrösse Ärztemuster',
	'0960': 'Kennzeichnung Gebührenpflichtig',
	'0961': 'Kennzeichnung aut idem',
	'0962': 'Kennzeichnung noctu',
	'0970': 'Anzahl (Packungen) Medikament auf Rezept',
	'0971': 'Anzahl (Packungen) Medikament auf Privatrezept',

	'2002': 'KASSENNAME für Albis (Quelle: mediSYS)',

	'2700': 'IK des Krankenhauses',
	'2701': 'Fachgebiet laut LKA',
	'2702': 'Arztnummer des Anästhesisten',
	'2706': 'Indikationsschlüssel',
	'2709': 'Lfd. OP-Nummer',
	'2710': 'Lfd. OP-Nummer',
	'2711': 'OP-Datum',
	'2720': 'Blutung',
	'2721': 'Narkosezwischenfall',
	'2722': 'Pneumonie',
	'2723': 'Wundinfektion',
	'2724': 'Gefäss- oder Nervenläsion',
	'2725': 'Lagerungsschäden',
	'2726': 'Venenthrombose',
	'2727': 'Komplikation',
	'2728': 'Erfolgsbeurteilung hinsichtlich Indikationsstellung',
	'2729': 'Erfolgsbeurteilung hinsichtlich Histologie',
	'2730': 'Revisionseingriff',
	'2731': 'Stationäre Aufnahme',
	'2732': 'Angaben zu implantierten Materialien',
	'2740': 'Art der Operation',
	'2741': 'Dauer der Operation',
	'2742': 'Operierte Seite',
	'2743': 'Art der Anästhesie',
	'2744': 'Art der Anästhesie gemäss Klassifikation Strukturvertrag',
	'2750': 'Operateur hat Facharztstatus',
	'2751': 'Anzahl ärztl. Assistenten bei OP',
	'2752': '(Ein) OP-Assistent hat Facharztstatus',
	'2753': 'Anzahl nichtärzticher Assistenten bei OP',
	'2760': 'Art der Anästhesie',
	'2761': 'Anästhesie erbracht',
	'2762': 'Dauer der Anästhesie',
	'2770': 'Blutung',
	'2771': 'Narkosezwischenfall',
	'2772': 'Pneumonie',
	'2773': 'Wundinfektion',
	'2774': 'Gefäss- oder Nervenläsion',
	'2775': 'Lagerungsschäden',
	'2776': 'Venenthrombose',
	'2780': 'Revisionseingriff erforderlich',
	'2781': 'Histologie',
	'2782': 'Stationäre Weiterbehandlung erforderlich',

	'3000': 'Patientennummer/-kennung',
	'3100': 'Namenszusatz/Vorsatzwort',
	'3101': 'Name des Patienten',
	'3102': 'Vorname des Patienten',
	'3103': 'Geburtsdatum des Patienten', 
	'3104': 'Titel des Patienten',
	'3105': 'Versichertennummer des Patienten',
	'3106': 'PLZ/Wohnort des Patienten',
	'3107': 'Strasse/Hausnummer des Patienten',
	'3108': 'Versichertenart MFR',				# 1=M,3=F,5=R
	'3110': 'Geschlecht des Patienten',			# 1=M,2=W
	'3111': 'Geburtsjahr des Patienten',
	'3112': 'PLZ des Patienten',
	'3113': 'Wohnort des Patienten',
	'3114': 'Wohnsitzländercode',
	'3116': 'KV-Bereich',
	'3150': 'Arbeitgeber',						# nur bei header 0191
	'3152': 'Unfallversicherungsträger',		# nur bei header 0191

	'3200': 'Namenszusatz/Vorsatzwort des Hauptversicherten',
	'3201': 'Name des Hauptversicherten',
	'3202': 'Vorname des Hauptversicherten',
	'3203': 'Geburtsdatum des Hauptversicherten',
	'3204': 'Wohnort des Hauptversicherten',
	'3205': 'Strasse des Hauptversicherten',
	'3206': 'Titel des Hauptversicherten oder Familienverhältnis',		# conflicting sources !
	'3207': 'PLZ des Hauptversicherten',
	'3208': 'Telefonnummer des Verletzten',		# nur bei header 0191
	'3209': 'Wohnort des Hauptversicherten',
	'3210': 'Geschlecht des Hauptversicherten',	# nur bei header 0191

	# Quelle: mediSYS GmbH
	'3301': '?? Name Patient',
	'3302': '?? Vorname Patient',
	'3303': '?? Patient geb.',
	'3308': '?? Status Patient',

	'3600': 'Patientennummer (alter BDT ?, beobachtet bei Medistar)',
	'3601': 'Röntgennummer',
	'3602': 'Archivnummer',
	'3603': 'BG-Nummer',
	'3610': 'Datum Patient seit',							# nur bei header 6100
	'3612': 'Datum Versichertenbeginn bei Kassenwechsel',	# nur bei header 6100
	'3620': 'Beruf des Patienten',							# nur bei header 6100
	'3622': 'Grösse des Patienten',							# nur bei header 6100
	'3623': 'Gewicht des Patienten',						# nur bei header 6100
	'3625': 'Arbeitgeber des Patienten',					# nur bei header 6100
	'3626': 'Telefonnummer des Patienten',					# nur bei header 6100
	'3627': 'Nationalität des Patienten',					# nur bei header 6100
	'3628': 'Muttersprache des Patienten',					# nur bei header 6100
	'3630': 'Arztnummer des Hausarztes',					# nur bei header 6100
	'3631': 'Entfernung Wohnung-Praxis',					# nur bei header 6100
	'3635': 'interne Zuordnung Arzt bei GP',				# nur bei header 6100
	'3637': 'Rezeptkennung',								# nur bei header 6100
	'3649': 'Dauerdiagnosen ab Datum',						# nur bei header 6100
	'3650': 'Dauerdiagnosen',								# nur bei header 6100
	'3651': 'Dauermedikamente ab Datum',					# nur bei header 6100
	'3652': 'Dauermedikamente',								# nur bei header 6100
	'3654': 'Risikofaktoren',								# nur bei header 6100
	'3656': 'Allergien',									# nur bei header 6100
	'3658': 'Unfälle',										# nur bei header 6100
	'3660': 'Operationen',									# nur bei header 6100
	'3662': 'Anamnese',										# nur bei header 6100
	'3664': 'Anzahl Geburten',								# nur bei header 6100
	'3666': 'Anzahl Kinder',								# nur bei header 6100
	'3668': 'Anzahl Schwangerschaften',						# nur bei header 6100
	'3670': 'Dauertherapie',								# nur bei header 6100
	'3672': 'Kontrolltermine',								# nur bei header 6100
	'3673': 'Dauerdiagnose (ICD-Code)',
	'3674': 'Diagnosensicherheit Dauerdiagnose',
	'3675': 'Seitenlokalisation Dauerdiagnose',

	'3700': 'Name erste freie Kategorie',					# nur bei header 6100
	'3701': 'Inhalt erste freie Kategorie',					# nur bei header 6100
	# 3704-3719 freie Kategorien

	'4101': 'Abrechnungsquartal',
	'4102': 'Ausstellungsdatum',
	'4103': 'Gültigkeit',
	'4104': 'VKNR, Kassennummer',
	'4105': 'Geschäftsstelle der VK',
	'4106': 'Kostenträger-Untergruppe (KTAB)',
	'4107': 'Abrechnungsart',
	'4109': 'KVK: letzte Vorlage (TTMMJJ)',
	'4110': 'KVK: Gültigkeit bis',
	'4111': 'Krankenkassennummer (IK)',
	'4112': 'KVK: Versichertenstatus',
	'4113': 'KVK: Ost/West-Status/DMP-Kennzeichnung',
	'4121': 'Gebührenordnung',
	'4122': 'Abrechnungsgebiet',
	'4123': 'Personenkreis/Untersuchungskategorie',
	'4124': 'SKT-Zusatzangaben',
	'4125': 'Gültigkeitszeitraum von ... bis ...',

	'4201': 'Ursache des Leidens',
	'4202': 'Unfall, Unfallfolgen',
	'4203': 'Früherkennung',
	'4205': 'MuVo-Datum',
	'4206': 'mutmasslicher Tag der Entbindung',
	'4207': 'Diagnose/Verdacht',
	'4209': 'erläuternder Text zur Überweisung',
	'4210': 'Ankreuzfeld LSR',
	'4211': 'Ankreuzfeld HAH',
	'4212': 'Ankreuzfeld ABO.RH',
	'4213': 'Ankreuzfeld AK',
	'4215': 'Konz. wegen (Text)',
	'4217': 'Vertragsarzt-Nr. des Erstveranlassers / Mit/Weiter (Text)',	# conflicting sources
	'4218': 'Überweisung von Arztnummer',
	'4219': 'Überweisung von anderen Ärzten / an Name',						# conflicting sources
	'4220': 'Überweisung an Fachgruppe',
	'4221': 'Kurativ // Präventiv / Sonstige Hilfen / bei belegärztlicher Behandlung',
	'4222': 'Kennziffer OI./O.II. // Prävention',							# conflicting sources
	'4223': 'Kennziffer OIII. // Sonstige Hilfen',							# conflicting sources
	'4224': 'AU bis',
	'4233': 'stationäre Behandlung von... bis...',
	'4234': 'anerkannte Psychotherapie',
	'4235': 'Datum des Anerkennungsbescheides',
	'4236': 'Klasse bei Behandlung',
	'4237': 'Krankenhausname',
	'4238': 'Krankenhausaufenthalt',
	'4239': 'Scheinuntergruppe',
	'4243': 'weiterbehandelnder Arzt',
	'4261': 'Kurart',
	'4262': 'Durchführung als Kompaktkur',
	'4263': 'genehmigte Kurdauer in Wochen',
	'4264': 'Anreisetag',
	'4265': 'Abreisetag',
	'4266': 'Kurabbruch am',
	'4267': 'Bewilligte Kurverlängerung in Wochen',
	'4268': 'Bewilligungsdatum Kurverlängerung',
	'4269': 'Verhaltenspräventive Massnahmen angeregt',
	'4270': 'Verhaltenspräventive Massnahmen durchgeführt',
	'4271': 'Kompaktkur nicht möglich',

	'4500': 'Unfalltag',
	'4501': 'Uhrzeit des Unfalls',
	'4502': 'Eingetroffen in Praxis am',
	'4503': 'Uhrzeit des Eintreffens',
	'4504': 'Beginn der Arbeitszeit',
	'4505': 'Unfallort',
	'4506': 'Beschäftigung als',
	'4507': 'Beschäftigung seit',
	'4508': 'Staatsangehörigkeit',
	'4509': 'Unfallbetrieb',
	'4510': 'Unfallhergang',
	'4512': 'Verhalten des Verletzten nach dem Unfall',
	'4513': 'Erstmalige Behandlung',
	'4514': 'Behandlung durch',
	'4515': 'Art der ersten ärztlichen Behandlung',
	'4520': 'Alkoholeinfluß',
	'4521': 'Anzeichen eines Alkoholeinflusses',
	'4522': 'Blutentnahme zum c2h5oh-Nachweis',
	'4530': 'Befund',
	'4540': 'Röntgenergebniss',
	'4550': 'Art etwaiger Versorgung durch D-Arzt',
	'4551': 'krankhafte Verändrungen unabhängig vom Unfall',
	'4552': 'Bedenken gegen Angaben',
	'4553': 'Art der Bedenken gegen Angaben',
	'4554': 'Bedenken gegen Arbeistunfall',
	'4555': 'Art der Bedenken gegen Arbeitsunfall',
	'4560': 'arbeitsfähig',
	'4561': 'wieder arbeitsfähig ab',
	'4562': 'AU ausgestellt',
	'4570': 'besondere Heilbehandlung erforderlich',
	'4571': 'besondere Heilbehandlung durch',
	'4572': 'Anschrift behandelnder Arzt',
	'4573': 'AU ab',
	'4574': 'voraussichliche Dauer der AU',
	'4580': 'Rechnungsart',
	'4581': 'allgemeine Heilbehandlung durch',
	'4582': 'AU über 3 Tage',
	'4583': 'AU bescheinigt als',
	'4584': 'Nachschau erforderlich',

	'4601': 'Rechnungsnummer',
	'4602': 'Rechnungsanschrift',
	'4603': 'überweisender Arzt',
	'4604': 'Rechnungsdatum',
	'4605': 'Endsumme',
	'4608': 'Abdingungserklärung vorhanden',
	'4611': 'Unterkonto Arzt',
	'4613': 'Anlage erforderlich',
	'4615': 'Kopfzeile',
	'4617': 'Fußzeile',

	'5000': 'Leistungstag',
	'5001': 'Gebührennummer',
	'5002': 'Art der Untersuchung',
	'5003': 'Empfänger des Briefes',
	'5004': 'Kilometer',
	'5005': 'Multiplikator / Anzahl GNR',
	'5006': 'Um-Uhrzeit',
	'5007': 'Bestellzeit-Ausführungszeit',
	'5008': 'Doppelkilometer',
	'5009': 'freier Begründungstext',
	'5010': 'Medikament als Begründung',
	'5011': 'Sachkosten-Bezeichnung',
	'5012': 'Sachkosten/Materialkosten in Cent',
	'5013': 'Prozent der Leistung',
	'5015': 'Organ',
	'5016': 'Name des Arztes',
	'5017': 'Besuchsort bei Hausbesuchen',
	'5018': 'Zone bei Besuchen',
	'5019': 'Erbringungsort,Standort des Gerätes',
	'5023': 'GO-Nummern-Zusatz',
	'5024': 'GNR-Zusatzkennzeichen für poststationär erbrachte Leistungen',
	'5060': 'Beschreibung der GNR',
	'5061': 'Gebühr',
	'5062': 'Faktor',
	'5063': 'Betrag',
	'5064': 'Endsumme Privatrechnung',
	'5090': 'Honorarbezeichnung',
	'5091': 'Gutachtenbezeichnung',

	'6000': 'Abrechnungsdiagnosen',
	'6001': 'ICD-Schlüssel',
	'6003': 'Diagnosensicherheit',
	'6004': 'Seitenlokalisation',
	'6005': 'Histologischer Befund bei Malignität',
	'6006': 'Diagnosenerläuterung',

	'6200': 'Behandlungsdaten gespeichert am',
	'6205': 'aktuelle Diagnose',
	'6210': 'Medikament verordnet auf Kassenrezept',
	'6211': 'Medikament verordnet auf Privatrezept',
	'6215': 'Ärztemuster',
	'6220': 'Befund',
	'6221': 'Fremdbefund',
	'6222': 'Laborbefund',
	'6225': 'Röntgenbefund',
	'6230': 'Blutdruck',
	'6240': 'Symptome',
	'6260': 'Therapie',
	'6265': 'physikalische Therapie',
	'6280': 'Überweisung Inhalt',
	'6285': 'AU Dauer (von - bis)',
	'6286': 'AU wegen',
	'6287': 'AU wegen (ICD-Code)',
	'6288': 'Diagnosesicherheit AU wegen',
	'6289': 'Seitenlokalisation AU wegen',
	'6290': 'Krankenhauseinweisung, Krankenhaus',
	'6291': 'Krankenhauseinweisung',
	'6292': 'Krankenhauseinweisung wegen (ICD-Code)',
	'6293': 'Diagnosesicherheit Krankenhauseinweisung wegen',
	'6294': 'Seitenlokalisation Krankenhauseinweisung wegen',

	'6300': 'Bescheinigung',
	'6301': 'Inhalt der Bescheinigung',
	'6306': 'Attest',
	'6307': 'Inhalt des Attestes',
	'6310': 'Name des Briefempfängers',
	'6311': 'Anrede',
	'6312': 'Strasse',
	'6313': 'PLZ',
	'6314': 'Wohnort',
	'6315': 'Schlusssatz',
	'6316': 'Telefonnummer',
	'6317': 'Telefax',
	'6319': 'Arztnummer/Arztident',
	'6320': 'Briefinhalt',
	'6325': 'Bild-Archivierungsnummer',
	'6326': 'Graphikformat',
	'6327': 'Bildinhalt',
	# 63xx und 63xx+1 belong to each other in pairs up to 6398/99
	'6330': 'freie Kategorie 1: Name',
	'6331': 'freie Kategorie 1: Inhalt',

	'7201':'AOK-DMP (D.M.): 1.-3. Stelle der Postleitzahl',
	'7202':'AOK-DMP (D.M.): Nummer des Diabetes-Paß',
	'7210':'AOK-DMP (D.M.): Datum der Erstmeldung',
	'7212':'AOK-DMP (D.M.): bereits v. SSP mitbetreut; 1=nein, 2=ja',
	'7215':'AOK-DMP (D.M.): Schulungsstatus; 1=nicht 2=geschult',
	'7216':'AOK-DMP (D.M.): Jahr der letzten Schulung; Vorgabe 1979',
	'7220':'AOK-DMP (D.M.): Schulung laut Vertrag durchgeführt; ja, nein',
	'7221':'AOK-DMP (D.M.): Begründung für keine Schulung; 1 bis 5',
	'7222':'AOK-DMP (D.M.): Klartext für Sonstige 7221 = 5',
	'7223':'AOK-DMP (D.M.): Schulungsprogramm; 1 bis 17',
	'7224':'AOK-DMP (D.M.): Schulungsinstitution; 1 bis 4',
	'7226':'AOK-DMP (D.M.): Schwangerschaft; 1=nein, 2=ja',
	'7227':'AOK-DMP (D.M.): Mitglied Selbsthilfegruppen; 1=nein, 2=ja',
	'7228':'AOK-DMP (D.M.): Überweisung SPP/HA veranlasst ?; 1=nein, 2=ja',
	'7229':'AOK-DMP (D.M.): Begründung für keine Überweisung;1 bis 4',
	'7230':'AOK-DMP (D.M.): Klartext Sonstiges 7229 = 5',

	'8000': 'Satzidentifikation >>===============',
	'8100': 'Satzlänge',

	'8301': 'UNBEKANNT Datum',       ## nicht in GDT 2.1 Specs (KS)
	'8302': 'UNBEKANNT Datum',       ## nicht in GDT 2.1 Specs (KS)
	'8303': 'UNBEKANNT Uhrzeit',     ## nicht in GDT 2.1 Specs (KS)
	'8310': 'Anforderungsnummer', 
	'8311': 'UNBEKANNT Integer lang',## nicht in GDT 2.1 Specs (KS)
	'8312': 'UNBEKANNT Integer kurz',## nicht in GDT 2.1 Specs (KS)
	'8315': 'GDT-ID Empfänger',
	'8316': 'GDT-ID Sender',
	'8320': 'Labor Bezeichnung',     ## nicht in GDT 2.1 Specs (KS)
	'8321': 'Labor Strasse',         ## nicht in GDT 2.1 Specs (KS)
	'8322': 'Labor PLZ',             ## nicht in GDT 2.1 Specs (KS)
	'8323': 'Labor Ort',             ## nicht in GDT 2.1 Specs (KS)

	'8401': 'Befundstatus, E=End,T=Teil,V=Vor,A=Archiv',
	'8402': 'Geräte-/Verfahrensspezifisches Kennfeld',
	'8403': 'Gebührenordnung',
	'8404': 'Kosten in Doppelpfennigen',
	'8406': 'Kosten in Cent',
	'8407': 'UNBEKANNT Flag 1|2',    ## nicht in GDT 2.1 Specs (KS)
	'8410': 'Test-Ident/LDT-Kürzel',
	'8411': 'Testbezeichnung',
	'8417': 'Zuordnung (A,D,T,L...) neu für KVT',
	'8418': 'Teststatus',
	'8420': 'Ergebnis-/Meßwert',
	'8421': 'Einheit',
	'8422': 'Grenzwert Indikator',
	'8428': 'Probematerial-Ident',
	'8429': 'Probenmaterial-Nummer',
	'8430': 'Probenmaterial-Bezeichnung',
	'8431': 'Material_Spezifikation',
	'8432': 'Abnahme-Datum',
	'8433': 'Abnahme-Zeit',
	'8440': 'Keim-Ident',
	'8441': 'Keim-Bezeichnung',
	'8442': 'Keim-Nummer',
	'8443': 'Methode der Resistenzbestimmung',
	'8444': 'Wirkstoff-Ident',
	'8445': 'Wirkstoff-Generic-Nummer',
	'8446': 'MHK/Breakpoint',
	'8447': 'Resistenz-Interpretation',
	'8460': 'Normalwert-Text',
	'8461': 'Normalwert untere Grenze',
	'8462': 'Normalwert obere Grenze',
	'8470': 'Anmerkung',
	'8480': 'Ergebnis-Text',
	'8485': 'Zielwert KVT',
	'8486': 'Ersteintritt',
	'8490': 'Abschluss-Zeile',

	'8609': 'Gebührenordung',
	'8990': 'Signatur',

	'9100': 'Arztnummer des Absenders',
	'9102': 'Empfänger',
	'9103': 'Erstellungsdatum, TTMMJJJJ',
	'9105': 'laufende Nummer Datenträger im Paket',
	'9106': 'verwendeter Zeichensatz, 1=7 / 2=8-bit-Code',
	'9115': 'Erstellungsdatum ADT-Datenpaket',
	'9116': 'Erstellungsdatum KADT-Datenpaket',
	'9117': 'Erstellungsdatum AODT-Datenpaket',
	'9118': 'Erstellungsdatum STDT-Datenpaket',
	'9132': 'enthaltene Datenpakete dieser Datei',
	'9202': 'Gesamtlänge Datenpaket (Byte)',
	'9203': 'Anzahl Datenträger im Paket',
	'9204': 'Abrechnungsquartal',
	'9206': 'Zeichensatz (encoding)',
	'9210': 'Version ADT-Satzbeschreibung',
	'9211': 'Version Satztabelle ADT',
	'9212': 'Version der Satzbeschreibung',
	'9213': 'Version BDT',
	'9218': 'Version GDT',
	'9233': 'GO-Stammdatei-Version',
	'9600': 'Archivierungsart, 1=Gesamt, 2=Zeitraum, 3=Quartal',
	'9601': 'Zeitraum der Speicherung, TTMMJJJJTTMMJJJJ',
	'9602': 'Beginn der Übertragung, HHMMSSCC',
	'9901': 'Systeminterner Parameter'

}
#--------------------------------------------------------------
# 8000
xdt_packet_type_map = {
	'0020': "========<< Anfang Datenträger >>========",
	'0021': "========<< Ende Datenträger >>========",
	'0022': "========<< Anfang Datenpaket >>========",
	'0023': "========<< Ende Datenpaket >>========",
	'0010': "========<< Praxisdaten >>========",
	'0101': "========<< Fall: Primärarzt >>========",
	'0102': "========<< Fall: Überweisung >>========",
	'0103': "========<< Fall: Belegarzt  >>========",
	'0104': "========<< Fall: Notfall/Dienst/Vertretung >>========",
	'0109': "========<< Kurärztliche Abrechnung >>========",
	'0190': "========<< Fall: Privat >>========",
	'0191': "========<< Fall: BG >>========",
	'0199': "========<< Fall: unstrukturiert >>========",
	'6100': "========<< Patientenstamm >>========",
	'6200': "========<< Behandlungsdaten >>========",
	'6302': "========>> GDT: Anforderung einer neuen Untersuchung >>========",
	'adt0': "========<< ADT-Datenpaket-Header >>========",
	'adt9': "========<< ADT-Datenpaket-Abschluss >>========",
	'con0': "========<< Container-Header >>========",
	'con9': "========<< Container-Abschluss >>========",
	'prax': "========<< Praxisdaten >>========",
	'kad0': "========<< KADT-Datenpaket-Header >>========",
	'kad9': "========<< KADT-Datenpaket-Abschluß >>========",
	'std0': "========<< STDT-Datenpaket-Header >>========",
	'std9': "========<< STDT-Datenpaket-Abschluß >>========",
	'st13': "========<< Statistiksatz >>========"
}
#--------------------------------------------------------------
# XDT:
# dob: ddmmyyyy
# gender: 1 - male, 2 - female

# patient record fields
name_xdtID_map = {
	'last name': '3101',
	'first name': '3102',
	'date of birth': '3103',
	'gender': '3110'
}
#    'city': '3106',\
#    'street': '3107',\

# sort of GNUmed compatible
map_gender_xdt2gm = {
	'1': 'm',
	'm': 'm',
	'M': 'm',
	'4': 'm',
	'2': 'f',
	'f': 'f',
	'W': 'f',
	'w': 'f',
	'5': 'f'
}

map_gender_gm2xdt = {
	'm': '1',
	'f': '2',
	'tm': '1',
	'tf': '2',
	'h': '?'
}

# LDT "gender", 8407
map_8407_2str = {
	'0': _('unknown gender'),
	'1': _('male'),
	'2': _('female'),
	'3': _('child'),
	'4': _('boy'),
	'5': _('girl'),
	'6': _('animal')
}

# xDT character code mapping : 9106
xdt_character_code_map = {
	'1': 'ASCII (DIN 66003/ISO 646)',
	'2': 'cp437 (8 Bit)',
	'3': 'ISO 8859-1/cp1252'
}

_charset_fields = [
	'9106',			# LDT
	'9206'			# GDT
]

_map_field2charset = {
	'9106': {
		'1': 'ascii',
		'2': 'cp437',
		'3': 'iso8859-1'
	},
	'9206': {
		'1': 'ascii',
		'2': 'cp437',
		'3': 'iso8859-1'
	}
}

# Archivierungsart : 9600
xdt_Archivierungsart_map = {
	'1': 'Speicherung Gesamtbestand',
	'2': 'Speicherung beliebiger Zeitraum',
	'3': 'Speicherung eines Quartals'
}
# Praxistyp : 0202
xdt_Praxistyp_map = {
	'1': 'Einzelpraxis',
	'2': 'Gemeinschaftspraxis',
	'3': 'Fachübergreifende GP',
	'4': 'Praxisgemeinschaft',
	'5': 'Fachübergreifende GP ohne Kennzeichen Leistung',
	'6': 'ermächtigter Arzt',
	'7': 'Krankenhaus oder ärztlich geleitete Einrichtung'
}
# Versichertenart MFR : 3108
xdt_Versichertenart_map = {
	'1': 'Mitglied',
	'3': 'Familienversicherter',
	'5': 'Rentner',
}
# Kostenträgeruntergruppe : 4106
xdt_Kostentraegeruntergruppe_map = {
	'00': 'default',
	'01': 'SVA(Sozialversicherungsabkommen)',
	'02': 'BVG(Bundesversorgungsgesetz)',
	'03': 'BEG(Bundesentschädigungsgesetz)',
	'04': 'Grenzgänger',
	'05': 'Rheinschiffer',
	'06': 'SHT(Sozialhilfeträger, ohne Asylstellen)',
	'07': 'BVFG(Bundesvertriebenengesetz)',
	'08': 'Asylstellen(AS)',
	'09': 'Schwangerschaftsabbrüche'
}
# Abrechnungsart : 4107
xdt_Abrechnungsart_map = {
	'1': 'PKA(Primärkassen)',
	'2': 'EKK(Ersatzkassen)',
	'3': 'SKT(Sonstige Kostenträger)',
}
# Ost/West-Status VK : 4113
xdt_Ost_West_Status_map = {
	'1': 'West',
	'6': 'BVG',
	'7': 'SVA',
	'8': 'SVA',
	'9': 'Ost',
	'M': 'eingeschriebene Versicherte in Disease-Management-Programmen für Diabetes mellitus Typ2 - RK West',
	'X': 'eingeschriebene Versicherte in Disease-Management-Programmen für Diabetes mellitus Typ2 - RK Ost',
	'A': 'eingeschriebene Versicherte in Disease-Management-Programmen für Brustkrebs - RK West',
	'C': 'eingeschriebene Versicherte in Disease-Management-Programmen für Brustkrebs - RK Ost',
}
# Gebührenordnung : 4121
xdt_Gebuehrenordnung_map = {
	'1': 'BMA',
	'2': 'E-GO',
	'3': 'GOA'
}
# Abrechnungsgebiet : 4122
xdt_Abrechnungsgebiet_map = {
	'00': 'kein besonderes Abrechnungsgebiet (Defaultwert)',
	'01': 'Dialyse-Arztkosten',
	'02': 'Dialyse-Sachkosten',
	'03': 'Methadon-Substitutionsbehandlung',
	'04': 'Grosse Psychotherapie',
	##'04': 'persönlich erbrachte Notfallleistungen durch ermächtigte Krankenhausärzte',
	'05': 'Verhaltenstherapie',
	##'05': 'sonstige Notfallleistungen durch ermächtigte Krankenhausärzte',
	'06': 'Fremde Zytologie',
	'07': 'Diabestesabrechnung',
	'08': 'Umweltmedizin',
	'09': 'Rheuma',
	'10': 'Hirnleistungsstörungen',
	'11': 'Kodex-Anhangsarzt',
	'12': 'Kodex-Arzt',
	'13': 'Kodex-Listenarzt',
	'14': 'Ambulantes Operieren'
}
# Ursache des Leidens : 4201
xdt_Ursache_des_Leidens_map = {
	'2': 'Unfall, Unfallfolgen',
	'3': 'Versorgungsleiden'
}
# Ankreuzfeld LSR, HAH, ABO.RH, AK
xdt_Ankreuzfeld_map = {
	'1': 'angekreuzt'
}
# Scheinuntergruppe
xdt_Scheinuntergruppe_map = {
	'00': 'Ambulante Behandlung (Defaultwert)',
	'20': 'Selbstaustellung',
	'21': 'Zielauftrag (Defaultwert bei Einsendepraxen)',
	'22': 'Rahmenauftrag',
	'23': 'Konsillaruntersuchung',
	'24': 'Mit/Weiterbehandlung (Defaultwert ausser bei Einsendepraxen)',
	'25': 'Überweisung aus anderen Gründen',
	'26': 'Stat. Mitbehandlung, Vergütung nach amb. Grundsätzen',
	'27': 'Überweisungs-/Abrechnungssschein für Laboratoriumsuntersuchungen als Auftragsleistung',
	'30': 'Belegärztliche Behandlung (Default bei SA 0103)',
	'31': 'Belegärztliche Mitbehandlung',
	'32': 'Urlaubs-/bzw. Krankheitsvertretung bei belegärztlicher Behandlung',
	'41': 'ärztlicher Notfalldienst',
	'42': 'Urlaubs-bzw. Krankheitsvertretung',
	'43': 'Notfall',
	'44': 'Notfalldienst bei Taxi',
	'45': 'Notarzt-/Rettungswagen (Rettungsdienst)',
	'46': 'Zentraler Notfalldienst',
	'90': 'default bei SA 0190',
	'91': 'Konsillaruntersuchung',
	'92': 'stat. Mitbehandlung Vergütung nach stat. Grundsätzen',
	'93': 'stat. Mitbehandlung Vergütung nach ambul. Grundsätzen',
	'94': 'belegärztliche Behandlung im Krankenhaus'
}
# Gesetzlicher Abzug zur stationären Behandlung gemäss Paragraph 6a GOA
xdt_gesetzlicher_Abzug_map = {
	'1': 'nein',
	'2': 'ja'
}
# Klasse bei stationärer Behandlung
xdt_Klasse_stationaere_Behandlung_map = {
	'1': 'Einbettzimmer',
	'2': 'Zweibettzimmer',
	'3': 'Mehrbettzimmmer'
}
# Rechnungsart
xdt_Rechnungsart_map = {
	'01': 'Privat',
	'20': 'KVB',
	'21': 'Bahn-Unfall',
	'30': 'Post',
	'31': 'Post-Unfall',
	'40': 'Allgemeines Heilverfahren',
	'41': 'Berufsgenossenschaft Heilverfahren',
	'50': 'Bundesknappschaft',
	'70': 'Justizvollzugsanstalt',
	'71': 'Jugendarbeitsschutz',
	'72': 'Landesversicherungsanstalt',
	'73': 'Bundesversicherungsanstalt für Angestellte',
	'74': 'Sozialamt',
	'75': 'Sozialgericht',
	'80': 'Studenten-Deutsche',
	'81': 'Studenten-Ausländer'
}
# Abdingungserklärung vorhanden
xdt_Abdingungserklaerung_map = {
	'1': 'nein',
	'2': 'ja'
}
# Anlage erforderlich
xdt_Anlage_erforderlich_map = {
	'1': 'nein',
	'2': 'ja'
}
#Alkoholeinfluss
xdt_Alkoholeinfluss_map = {
	'1': 'nein',
	'2': 'ja'
}
# Blutentnahme
xdt_Blutentnahme_map = {
	'1': 'nein',
	'2': 'ja'
}
# Bedenken gegen das Vorliegen eines Arbeitsunfalls
xdt_Arbeitsunfall_map = {
	'1': 'nein',
	'2': 'ja'
}
# arbeitsfähig
xdt_arbeitsfaehig_map = {
	'1': 'angekreuzt'
}
# Besondere Heilbehandlung erforderlich
xdt_Heilbehandlung_erforderlich_map = {
	'1': 'ambulant',
	'2': 'stationär'
}
# Besondere Heilbehandlung durch
xdt_Besondere_Heilbehandlung_durch_map = {
	'1': 'selbst',
	'2': 'anderer Durchgangsarzt'
}
# Allgemeine Heilbehandlung durch
xdt_Allgemeine_Heilbehandlung_durch_map = {
	'1': 'selbst',
	'2': 'anderer Arzt'
}
# AU über 3 Tage
xdt_AU_3Tage_map = {
	'1': 'angekreuzt'
}
# 8401: Befundstatus
xdt_Befundstatus_map = {
	'E': '(kompletter) Endbefund',
	'T': 'Teilbefund',
	'V': '(kompletter) Vorbefund',
	'A': 'Archivbefund',
	'N': 'Nachforderung'
}

map_Befundstatus_xdt2gm = {
	'E': _('final'),
	'T': _('partial'),
	'V': _('preliminary'),
	'A': _('final'),
	'N': _('final')
}

# Teststatus : 8418
xdt_Teststatus_map = {
	'B': _('already reported'),
	'K': _('corrected result'),
	'F': _('missing, reported later')
}

# Resistenzmethode
xdt_Resistenzmethode_map = {
	'1': 'Agardiffusion',
	'2': 'Agardilution',
	'3': 'MHK-Bestimmung',
	'4': 'Breakpoint-Bestimmung'
}
# Resistenz-Interpretation
xdt_Resistenzinterpretation_map = {
	'0': 'nicht getestet',
	'1': 'sensibel/wirksam',
	'2': 'mässig sensibel/schwach wirksam',
	'3': 'resistent/unwirksam',
	'4': 'wirksam in hohen Konzentrationen'
}
# enthaltene Datenpakete in dieser Datei : 9132
kvdt_enthaltene_Datenpakete_map = {
	'1': 'ADT-Datenpaket',
	'2': 'AODT-Datenpaket(roter Erhebungsbogen)',
	'3': 'Kurärztliches Abrechnungsdatenpaket',
	'4': 'AODT-Hessen-Datenpaket (grüner Erhebungsbogen der KV Hessen)',
	'5': 'STDT-Datenpaket'
}
#KV-Bereich : 3116
kvdt_KV_Bereich_map = {
	'01': 'Schleswig-Holstein',
	'02': 'Hamburg',
	'03': 'Bremen',
	'17': 'Niedersachsen',
	'20': 'Westfalen-Lippe',
	'38': 'Nordrhein',
	'46': 'Hessen',
	'47': 'Koblenz',
	'48': 'Rheinhessen',
	'49': 'Pfalz',
	'50': 'Trier',
	'55': 'Nordbaden',
	'60': 'Südbaden',
	'61': 'Nordwürtemberg',
	'62': 'Südwürtemberg',
	'71': 'Bayern',
	'72': 'Berlin',
	'73': 'Saarland',
	'74': 'KBV',
	'78': 'Mecklenburg-Vorpommern',
	'83': 'Brandenburg',
	'88': 'Sachsen-Anhalt',
	'98': 'Sachsen'
}
# Personenkreis / Untersuchungskategorie : 4123
kvdt_Personenkreis_Untersuchungskategorie_map = {
	'01': 'Beschädigter',
	'02': 'Schwerbeschädigter',
	'03': 'Angehöriger',
	'04': 'Hinterbliebener',
	'05': 'Pflegeperson',
	'06': 'Tauglichkeitsuntersuchung',
	'07': 'ärztl. Versorgung',
	'08': 'Bewerber',
	'09': 'Erstuntersuchung',
	'10': 'Nachuntersuchung',
	'11': 'Ergänzungsuntersuchung',
	'12': 'Verfolgte'
}
#Unfall, Unfallfolgen : 4202
kvdt_Unfallfolgen_map = {
	'1': 'ja'
}
#belegärztliche Behandlung : 4221
kvdt_belegaerztliche_Behandlung_map = {
	'1': 'kurativ',
	'2': 'präventiv',
	'3': 'sonstige Hilfen',
	'4': 'bei belegärztlicher Behandlung'
}
# anerkannte Psychotherapie : 4234
kvdt_anerkannte_Psychotherapie_map = {
	'1': 'ja'
}
# Abklärung somatischer Ursachen : 4236
kvdt_somatische_Ursachen_map = {
	'1': 'ja'
}
# GNR-Zusatzkennzeichen für poststationär erbrachte Leistungen : 5024
kvdt_Zusatzkennzeichen_poststationaere_Leistungen_map = {
	'N': 'poststationäre Leistung'	
}
# Diagnosensicherheit : 6003
kvdt_Diagnosensicherheit_map = {
	'V': 'Verdacht auf / zum Ausschluss von',
	'Z': 'Zustand nach',
	'A': 'ausgeschlossen'
}
# Seitenlokalisation : 6004
kvdt_Seitenlokalisation_map = {
	'R': 'rechts',
	'L': 'Links',
	'B': 'beiderseits'
}
# Empfänger : 9102
kvdt_Empfaenger_map = {
	'01': 'Schleswig-Holstein',
	'02': 'Hamburg',
	'03': 'Bremen',
	'06': 'Aurich',
	'07': 'Braunschweig',
	'08': 'Göttingen',
	'09': 'Hannover',
	'10': 'Hildesheim',
	'11': 'Lüneburg',
	'12': 'Oldenburg',
	'13': 'Osnabrück',
	'14': 'Stade',
	'15': 'Verden',
	'16': 'Wilhelmshaven',
	'18': 'Dortmund',
	'19': 'Münster',
	'20': 'KV Westfalen Lippe',
	'21': 'Aachen',
	'24': 'Düsseldorf',
	'25': 'Duisburg',
	'27': 'Köln',
	'28': 'Linker Niederrhein',
	'31': 'Ruhr',
	'37': 'Bergisch-Land',
	'39': 'Darmstadt',
	'40': 'Frankfurt/Main',
	'41': 'Giessen',
	'42': 'Kassel',
	'43': 'Limburg',
	'44': 'Marburg',
	'45': 'Wiesbaden',
	'47': 'Koblenz',
	'48': 'Rheinhessen',
	'49': 'Pfalz',
	'50': 'Trier',
	'52': 'Karlsruhe',
	'53': 'Mannheim',
	'54': 'Pforzheim',
	'56': 'Baden-Baden',
	'57': 'Freiburg',
	'58': 'Konstanz',
	'59': 'Offenburg',
	'61': 'Nord-Würtemberg',
	'62': 'Süd-Würtemberg',
	'63': 'München Sadt u. Land',
	'64': 'Oberbayern',
	'65': 'Oberfranken',
	'66': 'Mittelfranken',
	'67': 'Unterfranken',
	'68': 'Oberpfalz',
	'69': 'Niederbayern',
	'70': 'Schwaben',
	'72': 'Berlin',
	'73': 'Saarland',
	'78': 'Mecklenburg-Vorpommern',
	'79': 'Postdam',
	'80': 'Cottbus',
	'81': 'Frankfurt/Oder',
	'85': 'Magdeburg',
	'86': 'Halle',
	'87': 'Dessau',
	'89': 'Erfurt',
	'90': 'Gera',
	'91': 'Suhl',
	'94': 'Chemnitz',
	'95': 'Dresden',
	'96': 'Leipzig',
	'99': 'Bundesknappschaft'
}
# Facharztstatus Operateur / Assistent : 2750/2752
kvdt_Facharztstatus_map = {
	'0': 'nein',
	'1': 'ja'	
}
# Anästhesie erbracht : 2761
kvdt_Anaesthesie_erbracht_map = {
	'1': 'vom Operateur',
	'2': 'vom Anästhesisten'
}
# Blutung : 2770-2776,2720-2726
kvdt_Zwischenfall_map = {
	'0': 'nein',
	'1': 'intraoperativ',
	'2': 'postoperativ bis zum 12. Tag EIGENBEFUND',
	'3': 'postoperativ bis zum 12. Tag FREMDBEFUND'
}
# Revisionseingriff erforderlich : 2780
kvdt_Revisionseingriff_erforderlich_map = {
	'1': 'ja'
}
# Histologie : 2781,2729
kvdt_Histologie_map = {
	'0': 'nein',
	'1': 'ja'
}
# stationäre Weiterbehandlung erforderlich : 2782
kvdt_stationaere_Weiterbehandlung_map = {
	'1': 'unmittelbare Aufnahme zur Weiterbehandlung',
	'2': 'stationäre Aufnahme zur Weiterbehandlung bis zum 12.Tag'
}
# stationäre Aufnahme : 2731
kvdt_stationaere_Aufnahme_map = {
	'0': 'nein',
	'1': 'unmittelbare Aufnahme zur Weiterbehandlung',
	'2': 'stationäre Aufnahme zur Weiterbehandlung bis zum 12.Tag'
}
# Indikationsschlüssel : 2706
kvdt_Indikationsschluessel_map = {
	'0': 'keine Angabe'
}
# Komplikation : 2727
kvdt_Komplikation_map = {
	'0': 'keine Komplikation'
}
# Erfolgsbeurteilung hinsichtlich Indikationsstellung : 2728
kvdt_Erfolgsbeurteilung_Indikation_map = {
	'1': 'gut',
	'2': 'mittel',
	'3': 'schlecht',
	'4': 'nicht beurteilbar'
}
# Revisionseingriff: 2730
kvdt_Revisionseingriff_map = {
	'0': 'nein',
	'1': 'erforderlich'
}
# Angaben zu implantierten Materialien : 2732
kvdt_Implantat_map = {
	'00': 'keine Implantation',
	'01': 'Herzschrittmachertyp AAI-R',
	'02': 'Herzschrittmachertyp VVI-R',
	'03': 'Herzschrittmachertyp DDD-R',
	'04': 'Herzschrittmachertyp DVI-R',
	'05': 'Herzschrittmachertyp DDI-R',
	'06': 'Herzschrittmachertyp VDD-R',
	'09': 'sonstiger Herzschrittmachertyp',
	'11': 'PMMA-Linse',
	'12': 'Silicon-Linse',
	'13': 'Acryl-Linse'
}
# Operierte Seite : 2742
kvdt_operierte_Seite_map = {
	'0': 'keine Angabe',
	'1': 'links',
	'2': 'rechts',
	'3': 'beidseitig'
}
# Art der Anästhesie gemäß Klassifikation Strukturvertrag : 2744
kvdt_Anaesthesie_Art_map = {
	'1': 'Intubationsnarkose',
	'2': 'Spinalanästhesie',
	'3': 'Maskennarkose',
	'4': 'Stand-By',
	'5': 'Plexusanästhesie',
	'6': 'Periduralanästhesie',
	'7': 'intravenöse Region',
	'8': 'Lokalanästhesie',
	'9': 'Retrobulbär-/Peribulbäranästhesie'
}
# Kurart : 4261
kvdt_Kurart_map = {
	'1': 'Ambulante Vorsorgeleistung zur Krankheitsverhütung',
	'2': 'Ambulante Vorsorgeleistung bei bestehenden Krankheiten',
	'3': 'Ambulante Vorsorgeleistung für Kinder'
}
# Packungsgröße bei Kassenrezept und Privatrezept : 0917,0918
kvdt_Packungsgroesse_map = {
	'N1': 'Kleine Packung',
	'N2': 'Mittlere Packung',
	'N3': 'Große Packung',
	'kA': 'keine Angabe'
}
# Heilmittel : 0925
#kvdt_Heilmittel_map = {
#	'01': 'Massagetherapie',
#	'02': 'Bewegungstherapie',
#	'03': 'Krankengymnastik',
#	'04': 'Elektrotherapie',
#	'06': 'Thermotherapie(Wärme- und Kältetherapie)',
#	'08': 'Kohlensäurebäder',
#	'09': 'Inhalalationtherapie',
#	'10': 'Traktionsbehandlung',
#	'20': 'Stimmtherapie',
#	'25': 'Sprechtherapie',
#	'30': 'Sprachtherapie',
#	'35': 'Sprech- und/oder Sprachtherapie bei Kindern und Jugendlichen',
#	'40': 'Beschäftigungs- und Arbeitstherapie (Ergotherapie)',
#	'90': 'Sonstiges',
#}

# Kennzeichnung gebührenpflichtig, aut idem, noctu
kvdt_Kennzeichnung_map = {
	'0': 'nein',
	'1': 'ja'
}
#--------------------------------------------------------------
xdt_map_of_content_maps = {
	'0202': xdt_Praxistyp_map,
	'0917': kvdt_Packungsgroesse_map,
	'0918': kvdt_Packungsgroesse_map,
#	'0925': kvdt_Heilmittel_map,
	'0953': kvdt_Packungsgroesse_map,
	'0960': kvdt_Kennzeichnung_map,
	'0961': kvdt_Kennzeichnung_map,
	'0962': kvdt_Kennzeichnung_map,
	'2706': kvdt_Indikationsschluessel_map,
	'2720': kvdt_Zwischenfall_map,
	'2721': kvdt_Zwischenfall_map,
	'2722': kvdt_Zwischenfall_map,
	'2723': kvdt_Zwischenfall_map,
	'2724': kvdt_Zwischenfall_map,
	'2725': kvdt_Zwischenfall_map,
	'2726': kvdt_Zwischenfall_map,
	'2727': kvdt_Komplikation_map,
	'2728': kvdt_Erfolgsbeurteilung_Indikation_map,
	'2729': kvdt_Histologie_map,
	'2730': kvdt_Revisionseingriff_map,
	'2731': kvdt_stationaere_Aufnahme_map,
	'2732': kvdt_Implantat_map,
	'2742': kvdt_operierte_Seite_map,
	'2744': kvdt_Anaesthesie_Art_map,
	'2750': kvdt_Facharztstatus_map,
	'2752': kvdt_Facharztstatus_map,
	'2761': kvdt_Anaesthesie_erbracht_map,
	'2770': kvdt_Zwischenfall_map,
	'2771': kvdt_Zwischenfall_map,
	'2772': kvdt_Zwischenfall_map,
	'2773': kvdt_Zwischenfall_map,
	'2774': kvdt_Zwischenfall_map,
	'2775': kvdt_Zwischenfall_map,
	'2776': kvdt_Zwischenfall_map,
	'2780': kvdt_Revisionseingriff_erforderlich_map,
	'2781': kvdt_Histologie_map,
	'2782': kvdt_stationaere_Weiterbehandlung_map,
	'3108': xdt_Versichertenart_map,
	'3110': map_gender_xdt2gm,
	'3116': kvdt_KV_Bereich_map,
	'3674': kvdt_Diagnosensicherheit_map,
	'3675': kvdt_Seitenlokalisation_map,
	'4106': xdt_Kostentraegeruntergruppe_map,
	'4107': xdt_Abrechnungsart_map,
	'4113': xdt_Ost_West_Status_map,
	'4121': xdt_Gebuehrenordnung_map,
	'4122': xdt_Abrechnungsgebiet_map,
	'4123': kvdt_Personenkreis_Untersuchungskategorie_map,
	'4201': xdt_Ursache_des_Leidens_map,
	'4202': kvdt_Unfallfolgen_map,
	'4210': xdt_Ankreuzfeld_map,
	'4211': xdt_Ankreuzfeld_map,
	'4212': xdt_Ankreuzfeld_map,
	'4213': xdt_Ankreuzfeld_map,
	'4221': kvdt_belegaerztliche_Behandlung_map,
	'4234': kvdt_anerkannte_Psychotherapie_map,
	'4236': kvdt_somatische_Ursachen_map,
	'4239': xdt_Scheinuntergruppe_map,
	'4230': xdt_gesetzlicher_Abzug_map,
	'4236': xdt_Klasse_stationaere_Behandlung_map,
	'4261': kvdt_Kurart_map,
	'4580': xdt_Rechnungsart_map,
	'4608': xdt_Abdingungserklaerung_map,
	'4613': xdt_Anlage_erforderlich_map,
	'4520': xdt_Alkoholeinfluss_map,
	'4522': xdt_Blutentnahme_map,
	'4554': xdt_Arbeitsunfall_map,
	'4560': xdt_arbeitsfaehig_map,
	'4570': xdt_Heilbehandlung_erforderlich_map,
	'4571': xdt_Besondere_Heilbehandlung_durch_map,
	'4581': xdt_Allgemeine_Heilbehandlung_durch_map,
	'4582': xdt_AU_3Tage_map,
	'5024': kvdt_Zusatzkennzeichen_poststationaere_Leistungen_map,
	'6003': kvdt_Diagnosensicherheit_map,
	'6004': kvdt_Seitenlokalisation_map,
	'6288': kvdt_Diagnosensicherheit_map,
	'6289': kvdt_Seitenlokalisation_map,
	'6293': kvdt_Diagnosensicherheit_map,
	'6294': kvdt_Seitenlokalisation_map,
	'8000': xdt_packet_type_map,
	'8401': xdt_Befundstatus_map,
	'8418': xdt_Teststatus_map,
	'8443': xdt_Resistenzmethode_map,
	'8447': xdt_Resistenzinterpretation_map,
	'9102': kvdt_Empfaenger_map,
	'9106': xdt_character_code_map,
	'9132': kvdt_enthaltene_Datenpakete_map,
	'9600': xdt_Archivierungsart_map
}
#--------------------------------------------------------------
def xdt_8date2iso(date=None):
	"""DDMMYYYY -> YYYY-MM-DD"""
	return '%s-%s-%s' % (date[-4:], date[2:4], date[:2])
#==============================================================
# $Log: gmXdtMappings.py,v $
# Revision 1.41  2007-06-15 07:58:01  ncq
# - greatly improve the xDT mappings
#
# Revision 1.40  2007/05/14 10:37:31  ncq
# - recoded to utf8
#
# Revision 1.39  2007/03/10 15:13:05  ncq
# - improved mappings, added code 3600
#
# Revision 1.38  2007/02/21 10:29:43  ncq
# - map_gender_gm2xdt
#
# Revision 1.37  2007/01/21 15:13:46  ncq
# - add a few more codes
#
# Revision 1.36  2007/01/06 23:04:06  ncq
# - missing ","
#
# Revision 1.35  2007/01/04 22:50:35  ncq
# - add a mapping
#
# Revision 1.34  2006/12/27 16:39:57  ncq
# - a few more gender codes as used by Medistar
#
# Revision 1.33  2006/12/17 15:00:31  ncq
# - fixed typo
#
# Revision 1.32  2006/10/31 15:59:11  ncq
# - somewhat improved mappings
#
# Revision 1.31  2006/10/31 12:01:17  ncq
# - some xDT mappings provided by Kai Schmidt
#
# Revision 1.30  2006/10/30 16:41:12  ncq
# - add _charset_fields
#
# Revision 1.29  2006/10/08 10:48:28  ncq
# - teach xdt reader to derive encoding from gdt 6301 record
#
# Revision 1.28  2006/07/13 21:00:32  ncq
# - cleanup gender mappings
# - streamline cXdtPatient and improve test harness
#
# Revision 1.27  2005/12/27 17:40:19  ncq
# - define _()
#
# Revision 1.26  2004/06/25 12:37:20  ncq
# - eventually fix the import gmI18N issue
#
# Revision 1.25  2004/06/20 15:38:58  ncq
# - if epydoc can't handle a locally undefined _() it is broken
#
# Revision 1.24  2004/06/20 06:49:21  ihaywood
# changes required due to Epydoc's OCD
#
# Revision 1.23  2004/06/18 13:34:58  ncq
# - map a few more line types
#
# Revision 1.22  2004/06/09 14:36:17  ncq
# - cleanup
#
# Revision 1.21  2004/05/27 13:40:21  ihaywood
# more work on referrals, still not there yet
#
# Revision 1.20  2004/05/18 20:37:03  ncq
# - update befundstatus/teststatus maps
#
# Revision 1.19  2004/05/11 08:06:49  ncq
# - xdt_8date2iso()
#
# Revision 1.18  2004/04/21 15:27:38  ncq
# - map 8407 to string for ldt import
#
# Revision 1.17  2004/04/19 12:43:44  ncq
# - add Befundstatus mapping xdt <-> GnuMed
#
# Revision 1.16  2004/03/20 19:45:49  ncq
# - rename gender map
#
# Revision 1.15  2003/11/19 12:30:22  shilbert
# - corrected typos
#
# Revision 1.14  2003/11/17 10:56:34  sjtan
#
# synced and commiting.
#
# Revision 1.1  2003/10/23 06:02:38  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.13  2003/04/03 14:59:36  ncq
# - lots more maps ...
#
# Revision 1.12  2003/03/26 07:44:40  ncq
# - near-complete maps now
#
# Revision 1.11  2003/03/24 23:49:34  ncq
# - a huge heap of new mappings by Basti
#
# Revision 1.10  2003/02/19 15:57:57  ncq
# - better strings
#
# Revision 1.9  2003/02/19 15:23:44  ncq
# - a whole bunch of new mappings by Basti
#
# Revision 1.8  2003/02/19 12:27:42  ncq
# - map_of_maps -> map_of_content_maps
#
# Revision 1.7  2003/02/19 12:26:47  ncq
# - map of maps
#
# Revision 1.6  2003/02/17 23:31:02  ncq
# - added some patient related mappings
#
# Revision 1.5  2003/02/14 01:49:17  ncq
# - better strings
#
# Revision 1.4  2003/02/13 15:42:54  ncq
# - changed some strings
#
# Revision 1.3  2003/02/13 15:26:09  ncq
# - added mappings for content translation of Satzidentifikation
#
# Revision 1.2  2003/02/13 12:21:53  ncq
# - comment
#
# Revision 1.1  2003/02/13 12:21:26  ncq
# - first check in
#
