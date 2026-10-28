import json

def I(title, authors=(), page=None, section="article", pp=None, note=None):
    return {"title": title, "authors": list(authors), "page": page, "section": section,
            "pp_number": pp, "note": note}

def PP(n, title, authors, follows):
    return I(title, authors, None, "practice_point", n, f"Follows page {follows} (insert; no page number)")

def BR(editors, page, title="Book Reviews", label="Book Review Editor"):
    return I(title, [], page, "book_reviews", note=f"{label}: {', '.join(editors)}")

def ED(page, who="Diana S. Waite"):
    return I("Editor’s Note", [who], page, "editorial")

def GE(authors, page, title="Guest Editor’s Note"):
    return I(title, authors, page, "guest_editor")

def O(title, page, authors=(), note=None):
    return I(title, authors, page, "other", note=note)

BTHL = lambda p: O("Building Technology Heritage Library", p, ["Mike Jackson"], "recurring column")
DIR = lambda p: O("Directory of Advertisers", p)
MEM = lambda p: O("APT Membership Information", p)

F = []
def add(file, vol, issue, year, items, note=None):
    d = {"file": file, "volume": vol, "issue": issue, "year": year, "items": items}
    if note: d["note"] = note
    F.append(d)

add("23_TOC_49-1.txt", 49, "1", 2018, [
    ED(3),
    I("Notes on the Design, Construction, and Sales Practices of the Berlin Iron Bridge Company", ["Thomas E. Boothby"], 5),
    I("Restoration of Gottesman Hall at the New York Public Library", ["Tiffani Simple", "Jared M. Shoemaker"], 13),
    I("Experimental Studies on the Impact of Bird Excreta on Architectural Metals", ["Dirk H. R. Spennemann", "Maggie J. Watson"], 19),
    PP(17, "A Road Map to Structural Alterations in the International Existing Building Code", ["Lori Ferriss", "Michael J. Auren"], 28),
    I("Oil Springs, Ontario: The Living, Breathing Dinosaur", ["Charles Fairbank"], 37),
    I("Facade Restoration of Richard Morris Hunt’s Clark Hall in Cleveland, Ohio", ["James V. Banta"], 45),
    I("Alternative Weather Stripping for Historic Window Sash at Mount Vernon, Virginia", ["Steven Stuckey"], 51),
    BR(["Lesley Gilmore"], 59),
    DIR(60), BTHL(61), MEM(63),
])

add("24_TOC_APT_Bulletin_Volume46-1_Pg1_REV1.txt", 46, "1", 2015, [
    ED(2),
    GE(["Rosa Lowinger", "Kyle Normandin"], 2, "Guest Editors’ Note"),
    I("Foreword to Modern Metal Finishes", ["David Fixler"], 3, "editorial"),
    I("Metallurgy 102: Structure and Degradation of Metals", ["Alan Pense"], 5),
    I("A Survey of Historic Finishes for Architectural Aluminum, 1920-1960", ["Xsusha Flandro", "Helen M. Thomas-Haney"], 13),
    I("The “White Metals” of Early-Twentieth-Century American Architecture", ["Richard Pieper"], 23),
    PP(13, "Data Interpretation and Early Corrosion Test Program for Historic Concrete Buildings", ["Gina Crevello"], 28),
    I("Modern Metals: Finishes, Investigation, and Conservation Considerations", ["Jamie Clapper Morris", "Deborah Slaton"], 29),
    I("Aluminum Finishes in Postwar Architecture", ["Thomas C. Jester"], 41),
    BTHL(51),
    BR(["Frances Gale"], 53, title="Book Review"),
    DIR(54), MEM(55),
], note="Special Issue on Modern Metal Finishes")

add("25_TOC_Vol48_2.3.txt", 48, "2/3", 2017, [
    ED(3),
    GE(["David Fixler", "Kyle Normandin"], 4, "Guest Editors’ Note"),
    I("Toward APT Consensus Principles for Practice on Renewing Modernism", ["David Fixler"], 6),
    I("Changing World, Evolving Value: Historic Preservation toward 2050", ["Carl Elefante"], 9),
    I("Mitigating the Flooding Threat at Mies van der Rohe’s Farnsworth House in Plano, Illinois", ["Jenna Cellini Bresler"], 13),
    I("Architect O’Neil Ford’s Exploration of the Solar House in Texas", ["Lauren Weiss Bricker"], 21),
    I("Modernism on Main Street: The Dilemma of the Half-modern Building", ["Mike Jackson"], 29),
    I("Testing Vitrolite Adhesion: Structural Evaluation of Reattachment Methods for Historic Glass Panels", ["Jordan C. Dick", "Matthew B. Bronski"], 37),
    I("The Lightest Touch: Repairing Custom Mid-century Windows with a Limited Budget", ["John H. Cluver"], 45),
    I("Rehabilitation of the Art and Architecture Building at the University of Illinois at Chicago", ["Scott Utter", "Kelsey Shipton"], 53),
    I("Inside the Modern: The Conservation of 1950s–1970s Interiors in Montréal, Québec", ["Claudine Déom"], 59),
    I("George Nakashima’s Arts Building and Cloister: A Conservation and Management Plan", ["Cesar Bargues-Ballester", "William Whitaker", "Frank G. Matero"], 67),
    BR(["Frances Gale", "Lesley Gilmore"], 75, label="Book Review Editors"),
    DIR(76), BTHL(78), MEM(79),
], note="Special Issue on Modernism. 'Half-modern' kept with hyphen as printed (line break at 'Half-' / 'modern').")

add("26_TOC-39-1.txt", 39, "1", 2008, [
    I("Letter to the Editor", [], 3, "letter", note="no author listed in TOC"),
    O("In Memory of Jacques Dalibard, 1935-2007", 4, note="in memoriam; no author listed in TOC"),
    I("A Flood of Light: H. H. Richardson’s Great Western Staircase at the New York State Capitol", ["Niklas W. Vigener", "James Jamieson"], 9),
    I("Identification of 1850s Brown Zinc Paint Made with Franklinite and Zincite at the U.S. Capitol", ["Frank S. Welsh"], 17),
    PP(5, "Mortar Analysis Part 1: Mortar-Making Materials", ["Lorraine Schnabel"], 30),
    I("Fabricating and Installing Side-Lap Roof Shingles in Eastern Pennsylvania", ["James Houston", "John N. Fugelso"], 33),
    I("Rediscovering Sustainable Design Through Preservation: Bauhaus Apartments in Tel Aviv", ["Anat Geva"], 43),
    BR(["Robert A. Young"], 51),
    DIR(53), MEM(57), O("Endowment List", 58),
])

add("27_TOC-39-2-3.txt", 39, "2/3", 2008, [
    GE(["Pamela Jerome"], 3, "An Introduction to Authenticity in Preservation"),
    I("Origins and Influence of the Nara Document on Authenticity", ["Herb Stovel"], 9),
    I("From Warsaw to Mostar: The World Heritage Committee and Authenticity", ["Christina Cameron"], 19),
    I("Considering the Authenticity of Cultural Landscapes", ["Nora J. Mitchell"], 25),
    I("World-Heritage Historic Urban Landscapes: Defining and Protecting Authenticity", ["Gustavo F. Araoz"], 33),
    PP(6, "Architectural Finishes: Research and Analysis", ["Dorothy S. Krotzer"], 38),
    I("The Nara Grid: An Evaluation Scheme Based on the Nara Document on Authenticity", ["Koenraad Van Balen"], 39),
    I("Applying Authenticity to Cultural Landscapes", ["Mechtild Rössler"], 47),
    I("Regional Authenticity: An Argument for Reconstruction in Oceania", ["Jennifer Ko"], 55),
    I("Authenticity in Aboriginal Cultural Landscapes", ["Thomas D. Andrews", "Susan Buggey"], 63),
    DIR(72), MEM(73),
], note="Authenticity theme issue (no special-issue banner in TOC text); Pamela Jerome credited as Guest Editor.")

add("28_TOC-39-4.txt", 39, "4", 2008, [
    I("Letter to the Editor", [], 3, "letter", note="no author listed in TOC"),
    I("The Legacy of French Colonialism: Preservation in Morocco’s Fez Medina", ["Stacy E. Holden"], 5),
    I("Reproducing Historic Wallpapers at the Grand Opera House, Meridian, Mississippi", ["Christopher Mills"], 13),
    I("High-Calcium Lime Mortar: The Effects of Traditional Preparation and Curing", ["Dagmar Michoinová", "Pavla Rovnaníková"], 23),
    I("Appropriate Means to an Appropriate End: Industry, Modernism, and Preservation", ["David N. Fixler"], 31),
    I("Using Natural Resources for Ventilation: The Application of Badgirs in Preservation", ["Fatemeh Mehdizadeh Saradj"], 39),
    I("Grouting as a Strengthening Technique for Earthen Structures in Seismic Areas", ["Charu Chaudhry", "Koenraad Van Balen"], 47),
    O("Index to Volume 39", 57), O("Montreal Conference Sponsor List", 61), DIR(62), MEM(63),
])

add("29_TOC-40-1.txt", 40, "1", 2009, [
    I("Sustainable Heritage: Challenges and Strategies for the Twenty-First Century", ["May Cassar"], 3),
    I("The Use of Lasers for Cleaning Large Architectural Structures", ["Andrzej Dajnowski", "Adam Jenkins", "Andrew Lins"], 13),
    I("Mortar Injection: A Case Study of the Villa Medicis in Rome", ["Mary B. Brush", "Didier Repellin"], 25),
    I("Blanketing the Home: The Use of Thermal Insulation in American Housing, 1920–1945", ["Joanna Dowling"], 33),
    I("Analyzing Mortars and Stuccos at the College of Charleston: A Comprehensive Approach", ["Dorothy S. Krotzer", "John J. Walsh"], 41),
    I("Abandoned in the Wilderness: Survival and Rescue at the Adirondack Iron Works", ["Janet A. Null"], 49),
    I("Condition Evaluation of Facades of Nineteenth-Century New York City Walk-Ups", ["Mark Davis", "Dan Eschenasy"], 57),
    DIR(63),
])

add("30_TOC-40-2.txt", 40, "2", 2009, [
    I("A Grading Protocol for Structural Lumber and Timber in Historic Structures", ["Ronald W. Anthony", "Kimberly D. Dugan", "Deborah J. Anthony"], 3),
    I("An Analysis of the Thermal Performance of Repaired and Replacement Windows", ["Robert Score", "Bradford S. Carpenter"], 11),
    I("Sustainable Solutions for Historic Buildings: Geothermal Heat Pumps in Heritage Preservation", ["Thomas Perry", "Carl A. Jay"], 21),
    PP(7, "Mortar Analysis Part 2: Analytical Methods", ["Lorraine Schnabel"], 28),
    I("Did It Work? Post-Restoration Evaluation of Terra Cotta at Atlanta City Hall", ["Sven E. Thomasen"], 29),
    I("Conservation Treatments for Earthen Structures in the Western Himalayas of India", ["Charu Chaudhry", "Sandeep Sikka"], 35),
    I("Lee Nelson Award Winner 2008: Preservation of Modern Architecture", ["Theodore H. M. Prudon"], 45, note="Lee Nelson Book Award piece; classed as article"),
    BR(["Frances Gale"], 49),
    DIR(51), O("Endowment List", 52), MEM(54),
])

add("31_TOC-40-3-4.txt", 40, "3/4", 2009, [
    I("Introduction to the Fortieth-Anniversary Issue", ["Brian S. Robinson", "David G. Woodcock", "Diana S. Waite"], 3, "editorial"),
    I("Towards a New Era of Cultural-Heritage Recording and Documentation", ["Robert Warden"], 5),
    I("Safety and Building Codes: The Recent Past and Future for Historic Structures", ["Marilyn E. Kaplan"], 11),
    I("Sustainable Design in Historic Buildings: Foundations and the Future", ["Baird M. Smith", "Carl Elefante"], 19),
    I("Preservation Engineering: Past, Present, and Future", ["Derek Trelstad", "Robert Silman"], 27),
    I("Climate Change and Landscape Preservation: A Twenty-First-Century Conundrum", ["Robert Z. Melnick"], 35),
    I("Academic Preparation for Preservation Practice", ["David G. Woodcock"], 43),
    I("Making the Project Real: Changes in Delivery of Concept to Construction", ["Ronald D. Staley", "H. Thomas McGrath Jr.", "David C. Overholt", "Thomas R. Whitmore"], 51),
    I("Update on Building-Materials Research", ["Frances Gale", "Norman R. Weiss"], 59),
    I("Make No Small Plans: How Strategic Planning Shaped APT from 1995 to 2008", ["Natalie Bull"], 67),
    I("Dissemination of Knowledge through Publication", ["Diana S. Waite"], 73),
    O("APT Historical Supplement, 1968-2008", 77, note="no author listed in TOC"),
    O("Index to Volume 40", 83), DIR(85), MEM(87),
], note="Special Fortieth-Anniversary Issue")

add("32_TOC-41-1.txt", 41, "1", 2010, [
    ED(3),
    GE(["Walter Sedovic"], 3, "Coming of Age"),
    I("Saving Energy in Historic Buildings: Balancing Efficiency and Value", ["John H. Cluver", "Brad Randall"], 5),
    I("Green Home-Rating Systems: A Preservation Perspective", ["Mike Jackson"], 13),
    I("Sustainable Heritage Conservation: Pere Marquette Railroad Depot in Michigan", ["Ilene R. Tyler", "Ann K. Dilcher"], 21),
    PP(8, "Using Dry Ice for Spray-Paint Removal on Weathering Steel", ["Mary B. Brush"], 28),
    I("Thermal Performance of Traditional Windows and Low-Cost Energy-Saving Retrofits", ["Paul Baker", "Roger Curtis", "Craig Kennedy", "Chris Wood"], 29),
    I("Sustainability: The Case for Long-Term Service Life and Built-In Redundancy", ["Pamela Jerome"], 37),
    I("Teaching Sustainability to Preservation Students", ["Jeffrey Chusid"], 43),
    BR(["Frances Gale"], 51),
    DIR(54), MEM(55), O("Endowment List", 56),
], note="Special Issue on Sustainability")

add("33_TOC-41-2-3.txt", 41, "2/3", 2010, [
    I("Maintaining a Stable Environment: Vasa’s New Climate-Control System", ["Emma Hocker"], 3),
    I("Red “Staining” on Marble: Biological or Inorganic Origin?", ["Carol A. Grissom", "Claire Gervais", "Nicole C. Little", "Genevieve Bieniosek", "Robert J. Speakman"], 11),
    I("Fire Protection of the Las Flores Adobe in San Diego, California", ["Douglas Porter", "Nick Artim"], 21),
    I("Restoration of Akoustolith Tile at Saint John the Divine, New York City", ["Laura Buchner"], 27),
    PP(9, "Nondestructive Evaluation: Structural Performance of Masonry", ["Donald W. Harvey Jr.", "Michael P. Schuller"], 36),
    I("Cast Pyrex Glass Block: Illuminating Its History and Conservation Issues", ["Mary Jablonski"], 37),
    I("Using Ground-Penetrating Radar to Investigate Historic Masonry Buildings", ["James S. Mellett", "Shelley E. Smith"], 47),
    I("“First Principles” in Conservation: The UNESCO Asia-Pacific Heritage Awards", ["Richard A. Engelhardt"], 57),
    I("Book Review", [], 67, "book_reviews", note="Book Review Editor: Frances Gale. TOC prints page 67 for both Book Review and Directory of Advertisers."),
    DIR(67), MEM(69), O("Author Guidelines", 71),
])

add("34_TOC-41-4.txt", 41, "4", 2010, [
    O("Capturing the Past for Future Use: Documentation Symposium Program", 2),
    GE(["David G. Woodcock"], 3),
    I("Informed Conservation: The Place of Research and Documentation in Preservation", ["Kate Clark"], 5),
    I("Government Policy and Practice: Digital Conservation and Landscape Renewal", ["Caroline R. Alderson", "Beth L. Savage", "Charles Matta", "Calvin Kam", "Anne E. Weber"], 11),
    I("The Role of HABS in the Field of Architectural Documentation", ["Catherine C. Lavoie"], 19),
    I("Metric Survey for Preservation Uses: Past, Present, and Future", ["Paul Bryan"], 25),
    PP(10, "Nondestructive Evaluation: Wood", ["Ronald W. Anthony"], 30),
    I("Information Technology for Building Documentation", ["Kelly Streeter"], 33),
    I("Building Information Modeling for Constructing the Past and Its Future", ["David M. Foxe"], 39),
    I("From HABS to BIM: Personal Experiences, Thoughts, and Reflections", ["George C. Skarmeas"], 47),
    O("Index to Volume 41", 55), DIR(56), MEM(57),
], note="Special Issue on Documentation")

add("35_TOC-42-1.txt", 42, "1", 2011, [
    I("The Macrotube: An Inexpensive Device to Improve Photodocumentation of Surfaces", ["L. Brad Shotwell", "Joshua Freedland", "David A. Waugh"], 3),
    I("Millenary Earthen Architecture in the Tropical Lowlands of Mexico", ["Annick Daneels", "Luis Fernando Guerrero-Baca"], 11),
    I("Assessment, Analysis, and Management of Lenticular-Truss Bridges", ["Thomas E. Boothby"], 19),
    PP(11, "Mortar Analysis Part 3: Buying the Right Services", ["Lorraine Schnabel"], 30),
    I("Water Testing Stained Glass Windows at Saint Thomas Church, New York City", ["Julie L. Sloan"], 31),
    I("Hygrothermal Modeling of Brick Masonry Using Empirically Determined Properties", ["Vinay V. Badami"], 37),
    I("The Development of Hydraulic Mortars, Cement, and Concrete in Puerto Rico", ["Beatriz del Cueto"], 45),
    BR(["Frances Gale"], 54, title="Book Review"),
    O("Endowment List", 56), DIR(58), MEM(59),
])

add("36_TOC-42-2-3.txt", 42, "2/3", 2011, [
    GE(["Thomas C. Jester", "David N. Fixler"], 3, "Modern Heritage: Progress, Priorities, and Prognosis"),
    I("Reassessing the Recent Past: Tower Neighborhood Renewal in Toronto", ["Michael McClelland", "Graeme Stewart", "Asrai Ord"], 9),
    I("Modern Continuity: Seattle’s Magnolia Branch Library Renovation and Addition", ["David Strauss"], 15),
    I("Preservation of Modern-Era Office Buildings and Their Environmental Controls", ["Vanessa Fernandez"], 21),
    I("Sustainable Restoration of Yale University’s Art + Architecture Building", ["Russell M. Sanders", "Benjamin Shepherd", "Elizabeth Skowronek", "Alison Hoffmann"], 29),
    PP(12, "Conditions Glossaries as a Tool in the Survey Process: A Review of Several Glossaries", ["Evan Kopelson"], 36),
    I("Conserving Otto Piene’s Kinetic-Light Sculptures in the Hawaii State Capitol", ["Rosa Lowinger"], 39),
    I("Preserving Health: Modern Hospitals as Historic Places", ["Cameron Logan"], 45),
    I("The Modern Plaza: Making More from Less", ["Kenneth M. Itle", "Harry J. Hunderman"], 51),
    I("Reglazing Frank Lloyd Wright’s Solomon R. Guggenheim Museum in New York City", ["Angel Ayón", "William Rose"], 59),
    I("Conserving Twentieth-Century Built Heritage: A Bibliography", ["Susan MacDonald", "Gail Ostergren"], 67),
    BR(["Frances Gale"], 69),
    DIR(72), MEM(73),
], note="Special Issue on Modern Heritage")

add("37_TOC-42-4.txt", 42, "4", 2011, [
    I("Conservation of the Hollow Tree in Vancouver’s Stanley Park", ["Harold Kalman", "Lorne Whitehead"], 3),
    I("Investigation of Painted Wood at Mission San Miguel Arcangel in California", ["Douglas W. Porter", "Ronald W. Anthony", "Kimberly D. Dugan"], 13),
    I("Underneath the Historic D.C. Courthouse: Solving Building Foundation Challenges", ["James W. Shepherd", "Nicole Ferran"], 21),
    I("The House that Mather Built: The Rangers’ Club at Yosemite National Park", ["George Jaramillo"], 29),
    I("Early Electrical Wiring Systems in American Buildings, 1890-1930", ["LaLuce D. Mitchell"], 39),
    I("Improving Hygrothermal Performance of a Historic Building in British Columbia", ["John Dam"], 47),
    I("A Brief History of Lightning Protection and the Components of a Lightning-Protection System", ["Matthew Seymour"], 53),
    BR(["Frances Gale"], 57),
    O("Index to Volume 42", 60), DIR(62), MEM(63),
])

add("41_TOC_45_2-3.txt", 45, "2/3", 2014, [
    I("The Values-Based Approach to Cultural-Heritage Preservation", ["Pamela Jerome"], 3, note="opening piece of special issue; may function as guest editor's introduction but not labeled as such"),
    I("The Development of the Australia ICOMOS Burra Charter", ["Meredith Walker"], 9),
    I("Values in Heritage Conservation: A Project of The Getty Conservation Institute", ["Marta De la Torre"], 19),
    I("Values-Based Preservation, Civic Engagement, and the U.S. National Park Service", ["Barbara J. Little"], 25),
    I("Creativity and Conservation: Managing Significance at the Sydney Opera House", ["Sheridan Burke", "Susan Macdonald"], 31),
    I("Inhabiting Place: Social Significance in Practice in Australia", ["Chris Johnston"], 39),
    I("The Values-Based Approach for Cultural-Heritage Preservation in U.S. Public Parks", ["Suzanne Scheld", "Dana H. Taplin", "Setha M. Low"], 49),
    I("The Values and Benefits of Heritage: Do Economists Think about More than Money?", ["Gareth Maeer"], 57),
    I("Values-Based Heritage Management and the Heritage Lottery Fund in the UK", ["Kate Clark"], 65),
    BR(["Frances Gale"], 73),
    DIR(75),
    O("APT Building Technology Heritage Library", 77, ["Mike Jackson"], "recurring column"),
    MEM(79),
], note="Special Issue on Values-Based Preservation")

add("42_49.2-3_Table_of_Contents.txt", 49, "2/3", 2018, [
    ED(3),
    GE(["Dean Koga"], 4),
    I("APT’s Fifth Decade: Reaching Maturity and Facing the Future", ["Dean Koga"], 6),
    I("Emergence of the APT Technical Committees PETC, TCSP, TC-MH, TC-Doc", [], 15,
      note="No person named. The line 'PETC, TCSP, TC-MH, TC-Doc' sits where the author line normally is; kept in the title, but it may be a subtitle or a committee byline (checked against PDF)."),
    I("APT’s Student Scholarship Program Sets the Tone for the Future of APT", ["Lesley M. Gilmore", "Sue Ann Pemberton"], 25),
    O("APT Building Technology Heritage Library", 31, ["Mike Jackson"], "recurring column; placed among the feature articles in this issue's TOC"),
    I("Sustaining Historic Properties in an Era of Climate Change", ["Sharon C. Park"], 35),
    I("The Stewardship of Modern Heritage: Looking Forward", ["Kyle Normandin"], 45),
    I("Biofilms and Lichens on Eroded Marble Monuments: Reconsidering Cleaning", ["Judith M. Jacob", "Michaela Schmull", "Federica Villa"], 55),
    I("Phosphate Consolidants for Carbonate Stones", ["George W. Scherer", "Elisa Franzoni", "Enrico Sassoni", "Gabriela Graziani"], 61),
    I("Development of Professional Heritage Conservation Practice in North America", ["Julia Gersovitz", "Robert Silman", "Ronald D. Staley", "John G. Waite"], 69),
    O("APT Historical Supplement, 1968–2018", 80, ["Lonnie Hovey"]),
    DIR(89), MEM(91),
], note="Special Issue: APT’s 50th Anniversary. No book reviews listed.")

add("43_49.4_Table_of_Contents.txt", 49, "4", 2019, [
    ED(3),
    I("Performance Testing of Acid Stains on Historic Concrete", ["Alice Louise Gilmore", "Frank Matero"], 5),
    I("Completing a Nineteenth-Century Vision: Creating Monumental Portal Gates at Philadelphia City Hall", ["Nan R. Gutterman", "J. Scott Howell"], 16),
    I("“Insulation with Vision”: The Development of Insulated Glazing, 1930–1980", ["Thomas Leslie"], 23),
    I("Protecting and Preserving América Tropical in Downtown Los Angeles", ["Leslie Rainer", "Susan Macdonald"], 33),
    I("Conservation of the 180 Wellington Building Mosaic in Ottawa, Ontario", ["Kelly Caldwell", "Joseph Sembrat", "Mark Rabinowitz", "James Bourdeau", "Wendy Baker", "Eric Stein"], 43),
    BR(["Lesley Gilmore"], 54),
    DIR(56), BTHL(57), MEM(63),
])

add("44_50.1._Table_of_Contents.txt", 50, "1", 2019, [
    ED(3),
    GE(["Marilyn Kaplan"], 4),
    O("Summit on the Future of Codes and Historic Buildings", 5, ["Marilyn Kaplan", "Mike Jackson"], "listed in the front-matter column with the editor's notes, not among feature articles"),
    I("Applications and Validation of Building Performance Analysis for a Georgia Farmhouse", ["Julie Arnold", "Ramana Koti", "Susan Turner", "Sandeep Ahuja"], 7),
    I("Combating Condensation at the National Air and Space Museum", ["Richard Renaud", "Brian S. Rose"], 19),
    PP(18, "Classical Structural Analysis Methods for Historic Structures", ["Thomas E. Boothby"], 28),
    I("Insulating the Walls of Historic Buildings: A Systematic Review of Existing Guidance", ["Daniel S. Castele", "Amanda L. Webb"], 37),
    I("Energy, Hygrothermal, and Freeze-Thaw Considerations for Insulating Mass Masonry Walls", ["David Artigas", "Sean O’Brien"], 45),
    O("Lee Nelson Book Award 2018", 56),
    BR(["Lesley Gilmore"], 59),
    DIR(61), BTHL(62), MEM(63),
], note="Special Issue: Energy Performance of Historic Building Envelopes")

add("45_50.2-3_Contents.txt", 50, "2/3", 2019, [
    ED(3),
    I("The Granite Streets and Sidewalks of Lower Manhattan", ["Richard Pieper"], 5),
    I("Conserving Rwandan Genocide Memorials", ["Randall Mason"], 17),
    I("Lessons in Galvanic Cathodic Protection Technology from Soldier Field and the Franklin Avenue Bridge", ["Arne P. Johnson", "John S. Lawler", "Michael S. Murphy"], 27),
    PP(19, "Structural Hollow-Tile Flat-Arch Assemblies: A Guide for Assessment and Repair", ["Alex Vandenbergh", "Derek Trelstad", "Rebecca Buntrock"], 36),
    I("Improvements to Freeze-Thaw Resistance of Replication Mixes for Historic Mortars", ["Michael Edison", "Chad Lausberg"], 46),
    I("New Light on Baltimore’s Cathedral of Books", ["John A. Matteo", "Nicole Ferran"], 59),
    I("Early Brass Sash Locks in the United States", ["Steven Stuckey"], 67),
    BR(["Lesley Gilmore"], 73),
    DIR(77), BTHL(78), MEM(79),
])

add("46_50.4_Table_of_Contents.txt", 50, "4", 2020, [
    ED(3),
    GE(["Jenna C. Bresler", "Justin M. Spivey"], 4, "Guest Editors’ Note"),
    I("Keeping the Lights On: Challenges to the Conservation of Australia’s Electrical Heritage", ["MacLaren North"], 5),
    I("A Working Artifact: Restoration of a 1908 Manually Controlled Elevator in Toronto", ["Romas Bubelis"], 13),
    I("Measured Performance: Assessing Limit States of Structural Hollow-Tile Arches", ["Derek Trelstad", "Rebecca Buntrock", "Alex Vandenbergh"], 21),
    I("Conservation of Character-Defining Engineered Building Systems", ["Matthew S. Chalifoux"], 33),
    I("Clearing the Air: Ventilation at the Colt Patent Fire-Arms Factory in Hartford, Connecticut", ["Christopher Tavener"], 42),
    BR(["Lesley Gilmore"], 51),
    DIR(54), BTHL(56), O("Index", 58), MEM(63),
], note="Special Issue: Preservation Engineering")

add("47_51.1_Table_of_Contents.txt", 51, "1", 2020, [
    ED(3),
    GE(["Barbara A. Campagna", "Jill H. Gotthelf"], 4, "Guest Editors’ Note"),
    I("The Global Context for the Future of Preservation Technology", ["Bradshaw Hovey"], 5),
    I("The Next Fifty: Perspectives from the Next Generation", ["LaLuce Mitchell"], 9),
    I("Preservation Philosophy and Approaches: The Next Fifty", ["David G. Woodcock"], 13),
    I("Redefining Brutalism", ["Barbara A. Campagna"], 25),
    I("Climate Chaos and Heritage-Conservation Values: The Urgency for Action", ["Mark Thompson Brandt", "Cory Rouillard"], 37),
    I("The Paradox and Dilemma of Reconstruction: A Report from the 2018 College of Fellows Roundtable", ["Stephen J. Kelley", "Donald Friedman", "Kyle Normandin", "Pamela Jerome"], 49),
    BTHL(56),
    BR(["Lesley Gilmore", "Natascha Wiener"], 58, label="Book Review Co-Editors"),
    DIR(60), MEM(63),
], note="Special Issue: The Next Fifty Symposium")

add("48_51.2-3_Contents.txt", 51, "2/3", 2020, [
    ED(3),
    I("Restoring a Cast-Iron Secret at the National Museum of Natural History in Washington, D.C.", ["Carly Bond"], 5),
    I("Who Invented the Fitch Sash Fastener?", ["Michael F. Lynch"], 13),
    I("Seismic Retrofitting Using Local Materials and Expertise at a Church in Kuñotambo, Peru", ["Claudia Cancino", "Elena Macchioni", "Benjamin Marcus", "Juan Carlos Mellado", "Juan Carlos Menéndez"], 23),
    I("Sweet&Salt: Water and the Dutch", ["Tracy Metz"], 31, note="title printed as 'Sweet&Salt' (no spaces), checked against PDF"),
    PP(20, "Introduction to Mid-Range Terrestrial Laser Scanning", ["Warren Wilford"], 38),
    I("Querying the Products of Two Recording Techniques: Analog and Digital", ["Brent R. Fortenberry", "Amalia Leifeste"], 47),
    I("Rehabilitation of Exterior Stone Masonry at the Union Station Head House in Toronto", ["Hassan Saffarini"], 57),
    I("Moisture Analysis and Preservation Practice at Cockspur Island Lighthouse in Georgia", ["Paul Hardin Kapp", "Stephen E. Hartley"], 65),
    BTHL(71),
    BR(["Lesley Gilmore", "Natascha Wiener"], 72, label="Book Review Co-Editors"),
    DIR(74), O("Abstracts of Articles in Spanish", 76), MEM(79),
])

add("49_51.4_Contents.txt", 51, "4", 2020, [
    ED(3),
    GE(["W. (Bill) Wei"], 4),
    I("Protecting Stained-Glass Windows from Vibrations Caused by Construction Operations", ["Dean Koga", "Erica Morasset", "Raymond Pepi", "David Woodham"], 6),
    I("Structural Investigations of a Seventeenth-Century Staircase and Wall Paintings at Powis Castle, Wales", ["Siobhan Watts", "Richard Lithgow", "Gareth Sandham"], 13),
    I("Testing to Determine Allowable Vibration Limits at a Natural-History Museum in the Netherlands", ["W. (Bill) Wei", "Esther Dondorp"], 19),
    I("Earthquake-Damage Mitigation for Museum Collections: Basic Concepts and Approaches", ["Jerry Podany"], 27),
    I("A Blueprint for Managing Construction-Vibration Risk at Museums", ["Douglas Rudenko", "Mohamad Sharif", "Brian Warner"], 37),
    I("Vibration Mitigation and Sound Testing in SUE Hall at the Field Museum in Chicago", ["Arne Johnson", "Mohamed ElBatanouny", "William Simpson"], 45),
    BR(["Lesley Gilmore", "Natascha Wiener"], 51, label="Book Review Co-Editors"),
    DIR(54), BTHL(56), O("Index", 58), MEM(63),
], note="Special Issue: Mitigating Vibration Damage")

add("50_52.1_Contents.txt", 52, "1", 2021, [
    ED(3),
    I("Performance Testing of Acrylic-Amended Earthen Mortars at Wupatki National Monument in Arizona", ["Caroline Dickensheets", "Frank G. Matero"], 5),
    I("Testing the Flood Resilience of Traditional Building Assemblies", ["Jenifer Eggleston", "Jennifer C. Parker", "Mary F. Striegel", "Peter B. Stynoski", "Jennifer Wellock"], 15),
    PP(21, "Specifying Mortars under ASTM C1713: Standard Specification for Mortars for the Repair of Historic Masonry", ["John Wathne"], 26),
    I("The Reassembly of the Rideau Street Convent Chapel in Ottawa", ["Harold Kalman"], 35),
    I("Atlas Regained: Renewing a Modern Icon in Lima’s World Heritage District", ["Rosabella Alvarez-Calderón Silva-Santisteban", "David N. Fixler"], 44,
      note="first author's name wraps across two lines ('Rosabella Alvarez-Calderón' / 'Silva-Santisteban'); treated as one person"),
    BTHL(54),
    BR(["Lesley Gilmore", "Natascha Wiener"], 56, label="Book Review Co-Editors"),
    DIR(60), MEM(63),
])

add("51_52.2-3_Contents.txt", 52, "2/3", 2021, [
    ED(3),
    GE(["Rosa Lowinger", "Kyle Normandin"], 5, "Guest Editors’ Note"),
    I("Post-Disaster Amnesia: Lack of Mitigation Planning and Heritage Rationality in a Port-au-Prince Megaproject", ["Olsen Jean Julien"], 7),
    I("Preemptive Strategies and Collaboration for Emergency Planning: Lessons Learned at Vizcaya in Miami", ["Lauren Reynolds Hall"], 15),
    I("Sea-Level-Rise Modeling and Impact Assessment for Historic Coastal Communities", ["Sujin Kim", "Morris Hylton III"], 25),
    PP(22, "Analysis of Segmental and Semicircular Masonry Arches", ["Thomas E. Boothby"], 34),
    I("Storm-Surge Modeling for Assessing Vulnerability of Historic Buildings in Miami-Dade County, Florida", ["Sonia R. Chao", "Benjamin Ghansah"], 45),
    I("Building Rural Resilience: Community-Led Disaster Mitigation and Landscape Restoration in Emerging Nations", ["Stacy Crevello"], 53),
    BTHL(62),
    BR(["Lesley Gilmore", "Natascha Wiener"], 64, label="Book Review Co-Editors"),
    DIR(66), MEM(67),
], note="Special Issue: Disaster Mitigation. PP22 title printed 'Semi-/circular' across a line break; joined as 'Semicircular'.")

add("52_56.2+APT+Bulletin+TOC.txt", 56, "2", 2026, [
    ED(3, "Josie Madison"),
    I("The Evergreens Carriage House: A Case Study of Sustainable Reconstruction", ["Shantia Anderheggen"], 5),
    I("Surface Patching of Sandstone Using Colloidal Silica", ["Aliaksei Fedarenka"], 15),
    PP(31, "Seeing the Big Picture: Machine Learning Tools in Building Preservation Decisions", ["Rebecca Napolitano", "Joe Kallas"], 20),
    I("Assessing, Conserving, and Restoring Historic Neon Signs", ["Todd A. Matuszewicz"], 37),
    I("Durability of Desert Masonry Veneer at Frank Lloyd Wright’s Taliesin West", ["Frank Matero", "Siqi Zhao"], 47),
    BTHL(57),
    DIR(58),
    I("Reviews", [], 59, "book_reviews", note="headed 'Reviews' (not 'Book Reviews'); Co-Editors: Lesley M. Gilmore, Ilene R. Tyler"),
    MEM(63),
])

out = __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "build", "toc_parsed_b.json")
json.dump(F, open(out, "w"), ensure_ascii=False, indent=1)
print(len(F), "files", sum(len(f["items"]) for f in F), "items")
