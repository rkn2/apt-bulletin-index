import json
OUT = __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "build", "toc_parsed_a.json")

def I(title, authors=(), page=None, section="article", pp=None, note=None):
    return {"title": title, "authors": list(authors), "page": page, "section": section, "pp_number": pp, "note": note}

def PP(n, title, authors, follows):
    return I(title, authors, None, "practice_point", n, f"Follows page {follows} (insert; no page number)")

def ED(name, page): return I("Editor’s Note", [name], page, "editorial")
def GE(title, names, page): return I(title, names, page, "guest_editor")
def BTHL(page, title="Building Technology Heritage Library"): return I(title, ["Mike Jackson"], page, "other")
def BR(page, eds, label="Book Review Co-Editors"):
    return I("Book Reviews", [], page, "book_reviews", note=f"{label}: " + ", ".join(eds))
def DIR(page, note=None): return I("Directory of Advertisers", [], page, "other", note=note)
def MEM(page): return I("APT Membership Information", [], page, "other")
def IDX(title, page): return I(title, [], page, "other")

issues = []
def add(file, vol, iss, year, items, note=None):
    d = {"file": file, "volume": vol, "issue": iss, "year": year, "items": items}
    if note: d["note"] = note
    issues.append(d)

NI = "Chapter of the special-issue monograph “The Hidden History of Building Paper, 1868–1919”; TOC prints author Nigel Isaacs once for the whole issue"
add("01_55.1-2_TOC.txt", 55, "1/2", 2025, [
    ED("Josie Madison", 3),
    GE("Guest Editors’ Note", ["Elizabeth Corbin Murphy", "Frances Gale"], 5),
    I("Chapter 1: Introduction", ["Nigel Isaacs"], 7, note=NI),
    I("Chapter 2: Revolution, 1868–1883", ["Nigel Isaacs"], 15, note=NI),
    I("Chapter 3: Evolution of Major Market Players, 1876–1919", ["Nigel Isaacs"], 27, note=NI),
    I("Chapter 4: Protecting the Brand", ["Nigel Isaacs"], 49, note=NI),
    I("Chapter 5: Domochronology", ["Nigel Isaacs"], 73, note=NI),
    DIR(81), MEM(83),
], note="Special Issue: The Hidden History of Building Paper, 1868–1919. Year from © line.")

add("02_55.3_Bulletin_TOC.txt", 55, "3", 2025, [
    ED("Josie Madison", 3),
    I("In Memory of Hugh Clark Miller", ["Michael A. Tomlan"], 5, "other", note="In memoriam"),
    I("Reconstructing the Reconstructions: Preserving Concrete Churches in Picardy, France", ["Thomas E. Boothby"], 7),
    I("Dating Construction with Tree Rings and Sapwood When Felling Dates Are Unavailable", ["Darrin L. Rubino", "Sarah A. Malone", "Christopher Baas"], 15),
    I("Challenges in Concrete Conservation for the Central Market in Hong Kong", ["Vishal Joshi", "Pamela Jerome", "Sandeep Sikka", "Douglas Emilio", "Yuhui Ouyang"], 23),
    PP(28, "Opening the Drapes: Shedding Light on Draped-Mesh Cinder-Concrete Floor Slabs", ["Lauren P. Feinstein", "Kevin C. Poulin"], 30),
    I("Testing the Effects of Glyphosate Herbicide Alternatives on Historic Building Materials", ["Abigail Poe", "Catherine Cooper"], 39),
    I("Vernacular Preservation of the Postindustrial Landscape with Geospatial Technology", ["John D. M. Arnold", "Don Lafreniere"], 53),
    BTHL(60),
    BR(62, ["Lesley Gilmore", "Ilene R. Tyler"]),
    DIR(52, "Page printed as 52 (out of sequence; as printed)"),
    MEM(67),
], note="Year from © line.")

add("03_Graffiti_54-1-2_TOC.txt", 54, "1/2", 2024, [
    ED("Diana S. Waite", 3),
    GE("Guest Editors’ Note", ["Kelly Ciociola", "Stephanie Hoagland", "Sarah Holder"], 5),
    I("Paint in Paradise: Graffiti as a Tool in Preserving the Miami Marine Stadium", ["Rosa Lowinger", "Jason Loyd Clement"], 7),
    I("Battle Hall Historic Graffiti: Analysis of the Writing on the Wall", ["Frances Gale", "Izabella Z. Nuckels", "Tara A. Dudley", "Joseph G. Barabe"], 15),
    I("Names, Games, and Dames: Civil War Military Graffiti Conservation at Historic Blenheim", ["Mary Jablonski"], 23),
    I("Paint of Protest and Commemoration: A Berlin Wall Section at the United Nations", ["Brooke Russell", "Gillian Randell", "Mary Slater"], 33),
    PP(26, "Beyond Removal: Determining Significance for the Preservation of Graffiti", ["Stephanie Hoagland"], 40),
    I("Laser Techniques for the Removal of Graffiti in Remote Locations", ["Andrzej Dajnowski", "Bartek Dajnowski", "Jamie Morris"], 49),
    I("“Appropriately and Effectively”: A Graffiti Management Plan for Rapid Response Teams", ["Jocelyn Chan", "John D. Lesak", "Sarah E. Brummett", "Urmila Srinivasan"], 57),
    I("Lessons from the Global South: Community Engagement for Decolonization and Decarbonization", ["Yasmeen Lari"], 65),
    BTHL(73),
    DIR(73, "TOC prints 73 for both this and Building Technology Heritage Library"),
    BR(75, ["Lesley Gilmore", "Natascha Wiener"]),
    MEM(79),
], note="Special Issue: Graffiti. Text layer garbled by stray digits; verified against PDF. Year from © line.")

add("04_TOC_54(3-4).txt", 54, "3/4", 2025, [
    ED("Diana S. Waite", 3),
    GE("Guest Editor’s Note", ["Janet Parks"], 5),
    I("A Catalyst for Conservation: The Discovery of a Cemetery’s Archives", ["Susan Olsen"], 7),
    I("The Preservation Archive at Drayton Hall: The Role of Documentation in Preserving a Landmark", ["Patricia Lowe Smith"], 15),
    I("Preserving the Work of Frank Lloyd Wright through the Use of Archival Materials", ["John H. Waters"], 21),
    I("Digital Archiving of Underrepresented Heritage: Cabins of the Enslaved, LGBTQ+ Sites, and Rosenwald Schools", ["Benjamin Baaske", "Megan S. Reed", "Catherine Cooper", "Isabella Jones", "Jason Church"], 29),
    PP(27, "Upgrading Climate-Control Systems in Historic Buildings: An Integrated Design Thinking Approach", ["Cindy Cogil", "Steven Barrett"], 38),
    I("Architectural Archives: Actors and Objects in Heritage Preservation", ["Salvatore Aprea", "Barbara Galimberti"], 49),
    I("Suggestions for Searching for Architectural Archives", ["Janet Parks"], 59),
    BTHL(63),
    BR(65, ["Lesley Gilmore", "Ilene R. Tyler"]),
    IDX("Index to Volume LIV", 74),
    DIR(57, "Page printed as 57 (out of sequence; as printed)"),
    MEM(79),
], note="Special Issue: Architectural Archives. © 2025 printed (volume 54). Copy is a JSTOR download. Verified against PDF.")

add("05_TOC_55.4_Bulletin-4.txt", 55, "4", 2025, [
    ED("Josie Madison", 3),
    I("Rebuilding Notre-Dame: Lessons in Documentation for Heritage Conservation", ["Lindsay S. Cook"], 5),
    I("The Mysterious Deplated Finish: The Color of 1930s Aluminum", ["Preston Hull"], 13),
    PP(29, "Steel Window Restoration: Effective Strategies for Restoring and Upgrading Historic Steel Windows", ["Arthur Femenella Sr.", "Arthur Femenella Jr."], 22),
    I("The Frick Collection: Modernizing Circulation and Preserving a Historic Cornice", ["Kevin C. Poulin", "David A. Ribbans", "Lauren P. Feinstein", "Filippo Masetti"], 33),
    I("Monumental Failure: The Loss of Graffiti on Richmond’s Former Confederate Monuments", ["Bryan Clark Green"], 41),
    BTHL(49),
    BR(51, ["Lesley Gilmore", "Ilene R. Tyler"]),
    IDX("Index to Volume LV", 57),
    DIR(60), MEM(61),
], note="Year from © line.")

add("06_TOC_56.1_Bulletin.txt", 56, "1", 2026, [
    ED("Josie Madison", 3),
    GE("Guest Editors’ Note", ["Evanne St. Charles", "Lori Ferriss"], 5),
    I("In Memory of Frank G. Matero", ["Jeanne Marie Teutonico"], 6, "other", note="In memoriam"),
    I("Historic Buildings, Modern Goals: Navigating Decarbonization in Preservation", ["Nakita Reed", "Angela Wyrembelski"], 9),
    I("Aligning Building Performance Standards with Historic Preservation", ["Sean Denniston"], 19),
    PP(30, "Quantifying Embodied Carbon in Preservation", ["Lori Ferriss"], 26),
    I("Market One and the Stanley Center: Approaches to Decarbonization in Historic and Nonhistoric Buildings", ["Lyndley Kent"], 37),
    I("Guidance for the Embodied Carbon Accounting of Structural Interventions to Historic and Existing Structures", ["Eleanor Phetteplace", "Tim Michiels"], 45),
    DIR(53), BTHL(55),
    BR(57, ["Lesley Gilmore", "Ilene R. Tyler"]),
    MEM(63),
], note="Special Issue: Decarbonizing the Built Environment through Heritage. Year from © line.")

add("07_52.4_Contents.txt", 52, "4", 2022, [
    ED("Diana S. Waite", 3),
    GE("Guest Editor’s Note", ["Ronald W. Anthony"], 5),
    I("Plywood in Twentieth-Century Built Heritage: Considerations for Conservation", ["Suzana Radivojevic", "Chad Randl"], 7),
    I("Open-Web Wood Trusses: Wood Behavior under Unanticipated Loading Conditions", ["Ronald W. Anthony", "Brian D. Aschim"], 17),
    I("Purified Linseed Oil: Considerations for Use on Historic Wood", ["Erin Gibbs", "Katherine Wonson"], 25),
    I("Considering Modern Fire Codes in Replacing Wood-Shingle and Wood-Shake Roofing", ["Samuel Zabb-Parmley"], 33),
    I("Preservation of the Aerial Tramway at Keane Wonder Mine, Death Valley, California", ["Douglas Porter", "Michael Cotroneo"], 41),
    I("Hidden Queen-Post Trusses: Discovery, Analysis, and Repairs at Princeton Theological Seminary", ["Annabelle Radcliffe-Trenner", "Edmund P. Meade"], 49),
    I("Building Diplomacy: Preserving Wood at the U.S. Department of State’s Culturally Significant Properties Abroad", ["Lauren R. Hall", "John E. Dumsick"], 55),
    BTHL(64),
    BR(66, ["Lesley Gilmore", "Natascha Wiener"]),
    DIR(68),
    IDX("Volume 52 Index", 70),
    MEM(75),
], note="Special Issue: Wood. No Practice Points listed. Year from © line.")

add("08_53.1_Contents.txt", 53, "1", 2022, [
    ED("Diana S. Waite", 3),
    I("Active Infrared Thermography as a Nondestructive Investigative Tool to Locate Evidence of Historic Hardware", ["Lucy Midelfort"], 5, note="Text layer reads 55; PDF image shows 5"),
    I("Performance Testing of Coatings for Repairing Terra-Cotta Glaze Spalls", ["Lauren J. DiCenzo", "Carolyn L. Searls"], 13),
    I("“Things That Should Look Permanent Forever”: The Challenges of Preserving the Washington Metro", ["Zachary M. Schrag"], 19),
    PP(23, "Fire-Safety Approaches for Historic Buildings in the United States", ["Timothy R. Costello"], 28),
    I("Contested Monuments, A Critical Issue in Times of Turmoil: A Report from the 2021 College of Fellows Roundtable", ["Sharon C. Park", "Rosa Lowinger", "Beth L. Savage", "Theresa Pasqual", "Bryan Clark Green", "Brent Leggs"], 39),
    I("Rediscovering Clara Barton’s Missing Soldiers Office in Washington, D.C.", ["Caroline Alderson", "Jeff Greene"], 49),
    BTHL(57),
    I("Lee Nelson Book Award 2021", [], 58, "other"),
    BR(61, ["Lesley Gilmore", "Natascha Wiener"]),
    DIR(62), MEM(63),
], note="Year from © line (2022).")

add("09_53.2-3_Contents.txt", 53, "2/3", 2022, [
    ED("Diana S. Waite", 3),
    GE("Guest Editors’ Note", ["Chris Gembinski", "Lorraine Schnabel"], 5),
    I("Material Matters", ["Frank Matero"], 7),
    I("When the Material Becomes the Protagonist: Debating Reconstruction and Authenticity in Southern Europe", ["Shirley Cefai", "JoAnn Cassar"], 15),
    I("Investigations of Historic Finishes: Finding the Earliest Extant Color and More", ["Emily MacDonald-Korth"], 23),
    PP(24, "Versatility in Design: History, Installation, Assessment, and Repair of Terrazzo", ["Anne T. Sullivan"], 28),
    I("Retain, Reinforce, or Reclaim: Best Practices for Renovating Structural Wood Floors", ["Tim Michiels", "Dan Bergsagel"], 39),
    I("Substitute Materials and The Secretary of the Interior’s Standards", ["Brian Goeken"], 49),
    I("The Stylistic Evolution of Historic Cast Stone", ["Richard Pieper"], 57),
    I("Glazing Design for the Martin Luther King Jr. Memorial Library in Washington, D.C.", ["Rebecca Wong", "Martina Driscoll"], 65),
    BTHL(73),
    BR(75, ["Lesley Gilmore", "Natascha Wiener"]),
    DIR(78), MEM(79),
], note="Special Issue: Materials. Year from © line.")

add("10_Bulletin_53.4_Table_of_Contents.txt", 53, "4", 2023, [
    ED("Diana S. Waite", 3),
    I("Lake Huron Red Tails", ["Wayne R. Lusardi"], 5),
    I("Use of Advanced Documentation and Analysis Technologies at the Shaughnessy House Conservatory in Montréal", ["Morgan Matheson", "Michael Duric"], 11),
    I("Restoration of the Harlem Fire Watchtower", ["Robert Kornfeld", "Charles Van Winckle"], 21),
    PP(25, "Metals for Historic Roofing: An Update", ["Jeffrey S. Levine", "Remo R. Capolino", "Julie M. Palmer"], 28),
    I("Seismic Evaluation and Retrofit of Unreinforced-Masonry Buildings in Italy", ["Edmund P. Meade"], 39),
    BTHL(50),
    BR(51, ["Lesley Gilmore", "Natascha Wiener"]),
    IDX("Index to Volume LIII", 57),
    DIR(61), MEM(63),
], note="Year from © line (2023).")

BRE = "Book Review Editor"
add("11_1-2_TOC_45_1.txt", 45, "1", 2014, [
    GE("Guest Editors’ Note", ["Richard I. Ortega", "Justin M. Spivey"], 3),
    I("Nondestructive Evaluation (NDE) of Embedded Iron and Steel", ["Charles Bransby-Zachary", "George Ballard", "Avigail Charnov"], 5),
    I("Corrosion Assessments for Historic Steel-Frame, Masonry-Clad Buildings", ["Gina L. Crevello", "Paul A. Noyce"], 13),
    I("Seeing with Different Eyes: NDE of Embedded Steel at Yale University", ["Richard I. Ortega"], 21),
    I("Case Studies in the Repair of Masonry-Clad, Steel-Framed Buildings", ["Jim Dossett"], 27),
    I("Fire and Reconstruction at Lobato Bridge in New Mexico", ["Frederick R. Rutz", "Todd M. Riley", "Peter Foster"], 37),
    I("Early Curtain-Wall Buildings and the Higgins Armory Museum in Massachusetts", ["Sara E. Wermiel"], 43),
    I("Preservation in New York City: At the Pinnacle or on the Precipice?", ["Peg Breen"], 51),
    BR(59, ["Frances Gale"], BRE),
    DIR(60),
    BTHL(61, "APT Building Technology Heritage Library"),
    MEM(63),
], note="Special Issue on Iron and Steel. Issue number 1 from TOC text (filename prefix '1-2' is not the issue). No Editor’s Note listed. Year from © line.")

add("12_1-2_TOC_45_4.txt", 45, "4", 2014, [
    I("Conservation of Dalle de Verre at the New York Hall of Science", ["Raymond M. Pepi", "Laura Buchner", "Christopher Gembinski"], 3),
    I("Can the 1960s Single-Glazed Curtain Wall Be Saved?", ["Pamela Jerome", "Angel Ayón"], 13),
    I("Reinforcement of Nineteenth-Century Wide-Span Trusses in Two New York Landmarks", ["Eytan Solomon", "Alastair Elliott"], 21),
    I("Protection of Historic Buildings for Blast Loads", ["Timothy J. Beach", "Peggy Van Eepoel"], 27),
    I("Issues in Values-Based Management for Indigenous Cultural Heritage in Australia", ["Kristal Buckley", "Sharon Sullivan"], 35),
    I("Sustainability of Historic Building Systems: Anatolian Seljuk and Ottoman Hospitals", ["Gulsen Disli"], 45),
    BTHL(53, "APT Building Technology Heritage Library"),
    BR(55, ["Frances Gale"], BRE),
    DIR(57),
    I("Author Guidelines", [], 59, "other"),
    IDX("Index to Volume 45", 60),
    MEM(63),
], note="Issue number 4 from TOC text (filename prefix '1-2' is not the issue). No Editor’s Note listed. Year from © line.")

add("13_47_1TOC_for_APT_Website.txt", 47, "1", 2016, [
    ED("Diana S. Waite", 3),
    GE("Guest Editor’s Note", ["Nancy A. Rankin"], 5),
    I("Water Management for Traditional Buildings: Adaptation for a Changing Climate", ["Roger Curtis"], 8),
    I("Permafrost Thaw and Aboriginal Cultural Landscapes in the Gwich’in Region, Canada", ["Thomas D. Andrews", "Steven V. Kokelj", "Glen MacKay", "Julie Buysse", "Ingrid Kritsch", "Alestine Andre", "Trevor Lantz"], 15),
    I("Sea-Level Rise Vulnerability Assessment of Coastal Resources in New Hampshire", ["Benjamin Curran", "Michael Routhier", "Gopal Mulukutla"], 23),
    I("Climate Change and Non-mechanically Ventilated Historic Interiors", ["Peter Brimblecombe", "Caroline Brimblecombe"], 31),
    I("Planning before Disaster Strikes: An Introduction to Adaptation Strategies", ["Ann D. Horowitz"], 40),
    I("Energy Retrofit of Older Houses in Hot and Humid Climates", ["William Dupont", "Hazem Rashed-Ali", "Randall Manteufel", "Thomas Thomson", "Levi Sanciuc"], 50),
    BR(59, ["Frances Gale"], BRE),
    DIR(60),
    BTHL(62, "APT Building Technology Heritage Library"),
    MEM(63),
], note="Special Issue on Climate Change and Preservation Technology. Year from © line.")

add("14_47_2-3_TOC2.txt", 47, "2/3", 2016, [
    ED("Diana S. Waite", 3),
    GE("Guest Editor’s Note", ["Hugh C. Miller"], 5),
    I("Remembering Susan Buggey: A Pioneer in Heritage Conservation", ["Christina Cameron"], 6, note="Tribute"),
    I("List of Publications by Susan Buggey", [], 9, "other"),
    I("Contributions of Pioneers on the Shared Terrain of Culture and Nature", ["Nora Mitchell"], 11),
    I("From Historic to Cultural Landscapes under the Watch of Susan Buggey", ["John Zvonar"], 18),
    I("Restoring a Modern Landscape in the Anthropocene: Cornelia Hahn Oberlander", ["Susan Herrington"], 23, note="'Cornelia Hahn Oberlander' is part of the bold title in the PDF, not an author"),
    I("Cultural Traditions of Abandoned Rural Cultural Landscapes", ["Carrie J. Gregory"], 29),
    PP(15, "Architectural Terra Cotta", ["Edward Gerns", "Rachel Will"], 36),
    I("Time, Architecture, and Geography: Modeling the Past and Future of Cultural Landscapes", ["Jennifer Minner", "Jeffrey M. Chusid"], 49),
    I("Enhancing Conservation Tools for Natural Heritage in Historic Districts", ["Susan M. Ross"], 60),
    I("A Québec Case Study in the Repurposing of Declining Cultural Landscapes", ["Ron Williams"], 68),
    BR(75, ["Frances Gale"], BRE),
    DIR(76),
    BTHL(78, "APT Building Technology Heritage Library"),
    MEM(79),
], note="Special Issue on Cultural Landscapes: A Tribute to Susan Buggey. Year from © line.")

add("15_47_4_TOC.txt", 47, "4", 2016, [
    ED("Diana S. Waite", 3),
    I("U-value Monitoring of Infill Panels of a Fifteenth-century Dwelling in Herefordshire, UK", ["Christopher J. Whitman", "Oriel Prizeman"], 6),
    I("Hydraulic Mosaics and Concrete Blocks in the Spanish Caribbean", ["Beatriz del Cueto"], 15),
    I("Cleaning Terra Cotta: Recent Trends in Technical Research and Practice", ["Frank G. Matero", "Irene Matteini", "Reza Vatankhah"], 24),
    I("Conservation of the Alexander Hamilton Monument at Trinity Church in Lower Manhattan", ["Jennifer Schork"], 34),
    I("The Significance of Local Earthen Heritage: An Interdisciplinary Intervention in Northern Argentina", ["Carolina Rivet", "Julieta Barada"], 42),
    I("2015 Lee Nelson Book Award Winner", [], 51, "other"),
    BR(54, ["Frances Gale"], BRE),
    BTHL(57),
    DIR(58),
    IDX("Index", 59),
    MEM(63),
], note="No Practice Points listed. Year from © line.")

add("19_TOC_46.2-3.txt", 46, "2/3", 2015, [
    ED("Diana S. Waite", 3),
    I("The Djenné Mosque: World Heritage and Social Renewal in a West African Town", ["Trevor H. J. Marchand"], 4),
    I("Stabilizing Masonry with History and High-Tech", ["Lizzie Olson", "Derek Trelstad"], 16),
    I("Two Aesthetic-Movement Rooms: Research and Conservation", ["Claudia Kavenagh", "Raymond M. Pepi"], 26),
    I("Highland Park Ford Plant: Documentation and Redevelopment", ["Ilene R. Tyler"], 36),
    I("Wells Street Bridge in Chicago: A Moveable Monument Restored", ["Carolyn Andrews"], 46),
    I("Restoration of the Cast-in-Place Concrete at the New York Hall of Science", ["Laura N. Buchner", "Raymond M. Pepi"], 54),
    I("Vibration Limits for Historic Buildings and Art Collections", ["Arne P. Johnson", "W. Robert Hannen"], 66),
    BR(75, ["Frances Gale"], BRE),
    DIR(76),
    BTHL(78, "APT Building Technology Heritage Library"),
    MEM(79),
], note="No Practice Points listed. Year from © line.")

add("20_TOC_46.4.txt", 46, "4", 2015, [
    ED("Diana S. Waite", 3),
    I("Georgia Marble Repair at the Minnesota State Capitol", ["Paul Whitenack", "L. Brad Shotwell", "Michael J. Scheffler"], 10),
    I("Structural Assessment, Analysis, and Rehabilitation of a Masonry Aqueduct", ["Dennis McMullan", "Douglas Bond"], 18),
    PP(14, "Wood Preservatives: Considerations for Historic-Preservation Projects", ["Ronald W. Anthony", "Stan T. Lebow"], 28),
    I("The Making of the Nara Document on Authenticity", ["Christina Cameron", "Nobuko Inaba"], 30),
    I("Taos Pueblo Preservation Program", ["Luis Mountain Zamora", "Mary Kay Judy"], 38),
    BTHL(46, "APT Building Technology Heritage Library"),
    BR(47, ["Frances Gale"], BRE),
    DIR(48),
    IDX("Index to Volume XLVI", 51),
    MEM(55),
], note="Year from © line. Text file also contains a following ad page with a running head '44:2-3 2014' (ignored).")

add("21_TOC_48-4.txt", 48, "4", 2017, [
    ED("Diana S. Waite", 3),
    GE("Guest Editors’ Note", ["James Shepherd", "Chris Gray", "Mario Santana Quintero"], 4),
    I("Assessment of Earthquake Damage at the Washington National Cathedral", ["Matthew C. Farmer", "Kelsey E. Sheridan", "Jacqueline Devereaux"], 5),
    I("History through the Elemental Analysis of Materials and pXRF", ["Natalie Feinberg Lopez"], 13),
    I("Cultural-heritage Inventory Implementations: The Versatility of the Arches System", ["Carrie Barton", "Adam Cox", "Sara Delgadillo Cruz", "Janet Hansen"], 19),
    PP(16, "Assessment of Historic Concrete Structures", ["Ann Harrer", "Paul Gaudette"], 28),
    I("Digital Restoration of a South Carolina Landmark: 3D Visualization at Drayton Hall", ["Patricia Lowe Smith"], 37),
    I("A Practical Cultural Resource Survey Tool For Preservation", ["Andréa Livi Smith", "Martha Burtis"], 43),
    I("CIPA’s Mission: Digitally Documenting Cultural Heritage", ["Mario Santana Quintero", "Andreas Georgopoulos", "Efstratios Stylianidis", "José Luis Lerma", "Fabio Remondino"], 51),
    BR(55, ["Frances Gale", "Lesley Gilmore"]),
    DIR(56), BTHL(57), MEM(63),
], note="Special Issue on Documentation. Year from © line. Carrie Barton / Adam Cox printed on one line with a comma.")

json.dump(issues, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(issues), sum(len(i["items"]) for i in issues))
from collections import Counter
print(Counter(it["section"] for i in issues for it in i["items"]))
