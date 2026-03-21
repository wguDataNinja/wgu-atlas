"""
write_adjudication_results.py

Writes the LLM adjudication results for all 171 ambiguous_residual packets.
Each decision was made by the LLM reviewing the full context packet.

Output: data/program_guides/bridge/llm_packets/adjudication_results.json
"""

import json
import os
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKETS_IN = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "llm_packets", "packets.json")
RESULTS_OUT = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "llm_packets", "adjudication_results.json")

# ---------------------------------------------------------------------------
# Decision map: packet_id -> (selected_code, confidence, alt_possible, signal, rationale)
# ---------------------------------------------------------------------------

# Rationale templates keyed by (course_slug, decision_type)
R = {

# ------- Education: Elementary Disciplinary Literacy -------
# UG programs (BA/BS level): D690 is active 3CU for BA/BS elementary ed programs (introduced 2025-02);
# C732 inactive legacy 3CU for same UG programs (last_seen 2025-02); C733 inactive 3CU for MAT/grad programs;
# D164 inactive 2CU MAT legacy; D698 active 2CU for MAT Elementary Ed.
# D690 current_programs explicitly lists BA elementary ed families matching these UG guides.
"elem_disc_lit_ug": (
    "D690", "high", False, "legacy_vs_active_code_pattern",
    "D690 is the active 3CU Elementary Disciplinary Literacy course for BA/BS elementary education programs "
    "(current_programs includes BA Elementary Education family; first_seen 2025-02, last_seen 2026-03). "
    "C732 is the superseded 3CU legacy code for the same UG programs (last_seen 2025-02, zero current_programs). "
    "C733 is the legacy MAT-level 3CU code (now also inactive). "
    "D164 is the legacy 2CU MAT version; D698 is the active 2CU MAT version. "
    "This guide is undergraduate; degree-level and legacy-vs-active pattern both point to D690."
),

# MAT level: D698 active 2CU for MAT Elementary Ed
"elem_disc_lit_mat": (
    "D698", "high", False, "legacy_vs_active_code_pattern",
    "D698 is the active 2CU Elementary Disciplinary Literacy course for MAT Elementary Education programs "
    "(current_programs = Master of Arts in Teaching, Elementary Education; first_seen 2025-02). "
    "C732 and C733 are inactive legacy 3CU and 3CU codes; D164 is inactive legacy 2CU MAT code. "
    "D690 is the active UG (3CU) variant. This guide is graduate/MAT-level; D698 is the only active MAT-scoped candidate."
),

# ------- Education: Elementary Social Studies Methods -------
# UG: D674 active 3CU in BA elementary ed programs; C104 inactive legacy 3CU; D681 active 2CU MAT
"elem_soc_studies_ug": (
    "D674", "high", False, "legacy_vs_active_code_pattern",
    "D674 is the active 3CU Elementary Social Studies Methods for BA/BS elementary education programs "
    "(current_programs: BA Educational Studies in Elementary Education and Special Education; first_seen 2022-01). "
    "C104 is the legacy C-prefix code with zero current_programs (inactive in this cohort). "
    "D681 is the 2CU MAT-level variant for graduate programs. "
    "As a UG guide, D674 is the correct active 3CU code."
),

# ------- Education: Student Teaching I Elementary -------
# UG: D717 active 8CU for BA Elementary Education; D523 inactive 6CU UG legacy; D524/D737 are MAT variants
"st1_elem_ug": (
    "D717", "high", False, "legacy_vs_active_code_pattern",
    "D717 is the active 8CU Student Teaching I for BA Elementary Education programs "
    "(current_programs: Bachelor of Arts, Elementary Education; first_seen 2024-09). "
    "D523 is the superseded 6CU legacy UG code (last_seen 2024-09, zero current_programs). "
    "D524/D737 are the 4CU MAT-level variants (inactive and active respectively). "
    "D717 directly replaces D523 for UG elementary programs with an updated CU value."
),

# MAT: D737 active 4CU for MAT Elementary Ed
"st1_elem_mat": (
    "D737", "high", False, "legacy_vs_active_code_pattern",
    "D737 is the active 4CU Student Teaching I for MAT Elementary Education programs "
    "(current_programs: Master of Arts in Teaching, Elementary Education; first_seen 2024-09). "
    "D524 is the superseded 4CU MAT legacy code (last_seen 2024-08). "
    "D523/D717 are the UG (6CU/8CU) variants. D737 directly replaces D524 for MAT elementary programs."
),

# ------- Education: Student Teaching II Elementary -------
# UG: D718 active 8CU; D525 inactive 6CU UG legacy
"st2_elem_ug": (
    "D718", "high", False, "legacy_vs_active_code_pattern",
    "D718 is the active 8CU Student Teaching II for BA Elementary Education programs "
    "(current_programs: Bachelor of Arts, Elementary Education; first_seen 2024-09). "
    "D525 is the superseded 6CU UG legacy code (last_seen 2024-08, zero current_programs). "
    "D526/D738 are 4CU MAT variants. D718 directly replaces D525 for UG elementary programs."
),

# MAT: D738 active 4CU
"st2_elem_mat": (
    "D738", "high", False, "legacy_vs_active_code_pattern",
    "D738 is the active 4CU Student Teaching II for MAT Elementary Education programs "
    "(current_programs: Master of Arts in Teaching, Elementary Education; first_seen 2024-09). "
    "D526 is the superseded 4CU MAT legacy code (last_seen 2024-08). "
    "D525/D718 are the UG variants. D738 directly replaces D526 for MAT elementary programs."
),

# ------- Education: Student Teaching I Special Education -------
# UG: D719 active 8CU for BA Special Ed Mild to Moderate
"st1_sped_ug": (
    "D719", "high", False, "legacy_vs_active_code_pattern",
    "D719 is the active 8CU Student Teaching I for BA Special Education, Mild to Moderate programs "
    "(current_programs: Bachelor of Arts, Special Education, Mild to Moderate; first_seen 2024-10). "
    "D529 is the superseded 6CU UG legacy code (last_seen 2024-09, zero current_programs). "
    "D530/D739 are the 4CU MAT-level variants. D719 directly replaces D529 for UG special education programs."
),

# MAT: D739 active 4CU for MAT Special Education
"st1_sped_mat": (
    "D739", "high", False, "legacy_vs_active_code_pattern",
    "D739 is the active 4CU Student Teaching I for MAT Special Education programs "
    "(current_programs: Master of Arts in Teaching, Special Education; first_seen 2024-10). "
    "D530 is the superseded 4CU MAT legacy code (last_seen 2024-09, zero current_programs). "
    "D529/D719 are the UG (6CU/8CU) variants. D739 directly replaces D530 for MAT special education programs."
),

# ------- Education: Student Teaching II Special Education -------
# UG: D720 active 8CU
"st2_sped_ug": (
    "D720", "high", False, "legacy_vs_active_code_pattern",
    "D720 is the active 8CU Student Teaching II for BA Special Education, Mild to Moderate programs "
    "(current_programs: Bachelor of Arts, Special Education, Mild to Moderate; first_seen 2024-10). "
    "D531 is the superseded 6CU UG legacy code (last_seen 2024-09, zero current_programs). "
    "D532/D740 are 4CU MAT variants. D720 directly replaces D531 for UG special education programs."
),

# MAT: D740 active 4CU
"st2_sped_mat": (
    "D740", "high", False, "legacy_vs_active_code_pattern",
    "D740 is the active 4CU Student Teaching II for MAT Special Education programs "
    "(current_programs: Master of Arts in Teaching, Special Education; first_seen 2024-10). "
    "D532 is the superseded 4CU MAT legacy code (last_seen 2024-09, zero current_programs). "
    "D531/D720 are the UG variants. D740 directly replaces D532 for MAT special education programs."
),

# ------- Education: Secondary Disciplinary Literacy -------
# UG: D805 active 3CU for UG secondary ed programs (10 programs including BA/BS secondary ed families)
"sec_disc_lit_ug": (
    "D805", "high", False, "legacy_vs_active_code_pattern",
    "D805 is the active 3CU Secondary Disciplinary Literacy for BA/BS secondary education programs "
    "(current_programs: 10 programs including BA/BS Educational Studies in Secondary ed families; first_seen 2025-02). "
    "C728 is the superseded 3CU UG legacy code (last_seen 2025-02, zero current_programs). "
    "C729/D162 are inactive MAT-level variants (3CU/2CU); D806 is the active 2CU MAT variant. "
    "As a UG guide, D805 is the only active UG-scoped code."
),

# MAT: D806 active 2CU for MAT secondary programs
"sec_disc_lit_mat": (
    "D806", "high", False, "legacy_vs_active_code_pattern",
    "D806 is the active 2CU Secondary Disciplinary Literacy for MAT secondary education programs "
    "(current_programs: 7 programs including MAT English, Mathematics, Social Studies Secondary; first_seen 2025-02). "
    "C729/D162 are inactive MAT-level legacy codes (superseded by D806). "
    "C728 is the inactive UG 3CU legacy; D805 is the active UG 3CU variant. "
    "As a MAT/graduate guide, D806 is the only active MAT-scoped code."
),

# ------- Education: Student Teaching I Secondary -------
# UG: D721 active 8CU for BS secondary ed programs
"st1_sec_ug": (
    "D721", "high", False, "legacy_vs_active_code_pattern",
    "D721 is the active 8CU Student Teaching I for BS/BA secondary education programs "
    "(current_programs: 5 programs including BS Mathematics Education Secondary, BS Science Ed Secondary; first_seen 2025-02). "
    "D533 is the superseded 6CU UG legacy code (last_seen 2025-02, zero current_programs). "
    "D534/D741 are the 4CU MAT-level variants (inactive/active). D721 directly replaces D533 for UG secondary programs."
),

# MAT: D741 active 4CU
"st1_sec_mat": (
    "D741", "high", False, "legacy_vs_active_code_pattern",
    "D741 is the active 4CU Student Teaching I for MAT secondary education programs "
    "(current_programs: 7 programs including MAT English, Mathematics, Social Studies Secondary; first_seen 2025-02). "
    "D534 is the superseded 4CU MAT legacy code (last_seen 2025-02, zero current_programs). "
    "D533/D721 are the UG (6CU/8CU) variants. D741 directly replaces D534 for MAT secondary programs."
),

# ------- Education: Student Teaching II Secondary -------
# UG: D722 active 8CU
"st2_sec_ug": (
    "D722", "high", False, "legacy_vs_active_code_pattern",
    "D722 is the active 8CU Student Teaching II for BS/BA secondary education programs "
    "(current_programs: 5 programs including BS Mathematics Education Secondary, BS Science Ed Secondary; first_seen 2025-02). "
    "D535 is the superseded 6CU UG legacy code (zero current_programs). "
    "D536/D742 are 4CU MAT variants. D722 directly replaces D535 for UG secondary programs."
),

# MAT: D742 active 4CU
"st2_sec_mat": (
    "D742", "high", False, "legacy_vs_active_code_pattern",
    "D742 is the active 4CU Student Teaching II for MAT secondary education programs "
    "(current_programs: MAT English, Mathematics, Social Studies Secondary; first_seen 2025-02). "
    "D536 is the superseded 4CU MAT legacy code (zero current_programs). "
    "D535/D722 are the UG variants. D742 directly replaces D536 for MAT secondary programs."
),

# ------- Education Math: Advanced Calculus -------
# UG: D894 active 3CU for BA/BS secondary math ed; C885 inactive UG legacy; C886 active 2CU MAT
"adv_calc_ug": (
    "D894", "high", False, "legacy_vs_active_code_pattern",
    "D894 is the active 3CU Advanced Calculus for BA/BS secondary mathematics education programs "
    "(current_programs: BA Educational Studies in Secondary Mathematics Education, BS Mathematics Education Secondary; first_seen 2025-02). "
    "C885 is the superseded 3CU UG legacy code (last_seen 2025-01, zero current_programs). "
    "C886 is the active 2CU MAT-level variant (Master of Arts in Mathematics Education Secondary). "
    "D894 directly replaces C885 for UG math education programs."
),

# ------- Education Math: Algebra for Secondary Mathematics Teaching -------
# UG: D898 active 3CU; C879 inactive UG legacy; C880 active 2CU MA Math Ed; D904 active 2CU MAT
"alg_sec_math_ug": (
    "D898", "high", False, "legacy_vs_active_code_pattern",
    "D898 is the active 3CU Algebra for Secondary Mathematics Teaching for BA/BS secondary math ed programs "
    "(current_programs: BA Educational Studies in Secondary Mathematics Education, BS Mathematics Education Secondary; first_seen 2025-02). "
    "C879 is the superseded 3CU UG legacy code (last_seen 2025-02, zero current_programs). "
    "C880 is the active 2CU MA Math Education variant; D904 is the active 2CU MAT-level variant. "
    "D898 directly replaces C879 for UG math education programs."
),

# MAT: D904 active 2CU for MAT Math Ed Secondary
"alg_sec_math_mat": (
    "D904", "high", False, "legacy_vs_active_code_pattern",
    "D904 is the active 2CU Algebra for Secondary Mathematics Teaching for MAT Mathematics Education Secondary "
    "(current_programs: Master of Arts in Teaching, Mathematics Education Secondary; first_seen 2025-02). "
    "C880 is the active 2CU MA Mathematics Education variant (a different degree-type). "
    "C879 is the inactive UG 3CU legacy; D898 is the active UG 3CU variant. "
    "D904 is the only active code scoped to MAT-level programs for this course."
),

# ------- Education Math: Calculus I -------
# UG: D890 active 3CU for BA/BS secondary math ed; C282/C362/C363/C958/QJT2 are alternatives
"calc1_ug": (
    "D890", "high", False, "legacy_vs_active_code_pattern",
    "D890 is the active 3CU Calculus I for BA/BS secondary mathematics/physics education programs "
    "(current_programs: BA Educational Studies in Secondary Mathematics Education and Physics; first_seen 2025-02). "
    "C282 and C362 are the superseded C-prefix UG legacy codes (both last_seen ~2025-01, zero current_programs). "
    "C363/QJT2 are 2CU MA Math Education variants (graduate); C958 is active but scoped to BSCS (Computer Science). "
    "D890 directly replaces C282/C362 for UG math/physics education programs."
),

# ------- Education Math: Calculus II -------
# UG: D891 active 3CU; C283 inactive UG legacy; CQC2 active 2CU MA Math Ed
"calc2_ug": (
    "D891", "high", False, "legacy_vs_active_code_pattern",
    "D891 is the active 3CU Calculus II for BA/BS secondary mathematics education programs "
    "(current_programs: BA Educational Studies in Secondary Mathematics Education, BS Mathematics Education Secondary; first_seen 2025-02). "
    "C283 is the superseded 3CU UG legacy code (last_seen 2025-01, zero current_programs). "
    "CQC2 is the active 2CU MA Mathematics Education variant (graduate). "
    "D891 directly replaces C283 for UG math education programs."
),

# ------- Education Math: Linear Algebra -------
# UG: D893 active 3CU; RKT1 inactive UG legacy; RKT2 active 2CU MA Math Ed
"lin_alg_ug": (
    "D893", "high", False, "legacy_vs_active_code_pattern",
    "D893 is the active 3CU Linear Algebra for BA/BS secondary mathematics education programs "
    "(current_programs: BA Educational Studies in Secondary Mathematics Education, BS Mathematics Education Secondary; first_seen 2025-02). "
    "RKT1 is the superseded 3CU UG legacy code (last_seen 2025-01, zero current_programs). "
    "RKT2 is the active 2CU MA Mathematics Education variant (graduate). "
    "D893 directly replaces RKT1 for UG math education programs."
),

# ------- Education Science: General Chemistry II with Lab -------
# UG: D866 active 4CU; C374 inactive UG legacy; C673 active 3CU MA Sci Ed
"gen_chem2_ug": (
    "D866", "high", False, "legacy_vs_active_code_pattern",
    "D866 is the active 4CU General Chemistry II with Lab for BA/BS secondary chemistry education programs "
    "(current_programs: BA Educational Studies in Secondary Chemistry Science Education, BS Science Ed Secondary Chemistry; first_seen 2025-02). "
    "C374 is the superseded 4CU UG legacy code (last_seen 2025-01, zero current_programs). "
    "C673 is the active 3CU MA Science Ed Secondary Chemistry variant (graduate-only). "
    "D866 directly replaces C374 for UG chemistry education programs."
),

# ------- Education Science: Organic Chemistry -------
# UG: D867 active 3CU; UQT1 inactive UG legacy; AIT2 active 2CU MA Sci Ed
"org_chem_ug": (
    "D867", "high", False, "legacy_vs_active_code_pattern",
    "D867 is the active 3CU Organic Chemistry for BA/BS secondary chemistry education programs "
    "(current_programs: BA Educational Studies in Secondary Chemistry Science Education, BS Science Ed Secondary Chemistry; first_seen 2025-02). "
    "UQT1 is the superseded 3CU UG legacy code (last_seen 2025-01, zero current_programs). "
    "AIT2 is the active 2CU MA Science Education Secondary Chemistry variant (graduate-only). "
    "D867 directly replaces UQT1 for UG chemistry education programs."
),

# ------- Education Science: Astronomy -------
# UG: D852 active 3CU; C894 inactive UG legacy; C895 active 2CU MA Sci Ed
"astronomy_ug": (
    "D852", "high", False, "legacy_vs_active_code_pattern",
    "D852 is the active 3CU Astronomy for BA/BS secondary earth science education programs "
    "(current_programs: BA Educational Studies in Secondary Earth Science Education, BS Science Ed Secondary Earth Science; first_seen 2025-02). "
    "C894 is the superseded 3CU UG legacy code (last_seen 2025-02, zero current_programs). "
    "C895 is the active 2CU MA Science Education variant for graduate programs. "
    "D852 directly replaces C894 for UG earth science education programs."
),

# ------- IT: Business of IT Applications -------
# BSCS/BSCSIA/BSIT: D336 active 4CU (12 programs incl BSCNE/BSCSIA/SWE); C179 BSITM-only; C846 inactive
"biz_it_apps_d336": (
    "D336", "high", False, "program_name_fuzzy_match",
    "D336 is the active 4CU Business of IT - Applications for the CS/IT program family "
    "(current_programs: 12 programs including BSCNE, BSCSIA, SWE variants; first_seen 2022-05). "
    "C179 is active but exclusively scoped to Bachelor of Science, Information Technology Management (BSITM) — "
    "a different program from BSCS/BSCSIA/BSIT. C846 is inactive with zero current_programs. "
    "The AoS neighbor pattern (D-prefix codes) confirms this guide uses the D336 cohort, not C179."
),

# BSITM: C179 active 4CU exclusively in BSITM
"biz_it_apps_c179": (
    "C179", "high", False, "program_name_fuzzy_match",
    "C179 is the active 4CU Business of IT - Applications exclusively scoped to Bachelor of Science, "
    "Information Technology Management (current_programs: BSITM only; perpetual stability; first_seen 2017-01). "
    "D336 is active but scoped to BSCNE/BSCSIA/SWE programs — different program family from BSITM. "
    "C846 is inactive with zero current_programs. "
    "C179's current_programs directly matches this BSITM guide."
),

# ------- IT: Data Management Foundations -------
# BSCS/BSCSIA/BSIT: D426 active 3CU (13 programs); C175 BSITM-only; D323 inactive single-observation
"data_mgmt_d426": (
    "D426", "high", False, "program_name_fuzzy_match",
    "D426 is the active 3CU Data Management - Foundations for the CS/IT program family "
    "(current_programs: 13 programs including BSCNE, BSCSIA, SWE variants; first_seen 2022-06). "
    "C175 is active but exclusively scoped to BSITM — a different program. "
    "D323 has zero current_programs and was observed only in a single edition (2022-05, inactive). "
    "The AoS neighbor pattern confirms D-prefix usage; C175 is the BSITM-only variant."
),

# BSITM: C175 active 3CU exclusively in BSITM
"data_mgmt_c175": (
    "C175", "high", False, "program_name_fuzzy_match",
    "C175 is the active 3CU Data Management - Foundations exclusively scoped to BSITM "
    "(current_programs: Bachelor of Science, Information Technology Management; perpetual stability). "
    "D426 is active but scoped to BSCNE/BSCSIA/SWE programs. "
    "D323 has a single observation (2022-05) and zero current_programs — effectively inactive. "
    "C175 directly matches this BSITM guide."
),

# ------- IT: Network and Security Foundations -------
# BSCS/BSCSIA/BSIT: D315 active 3CU (12 programs); C172 BSITM-only
"net_sec_found_d315": (
    "D315", "high", False, "program_name_fuzzy_match",
    "D315 is the active 3CU Network and Security - Foundations for the CS/IT program family "
    "(current_programs: 12 programs including BSCNE, BSCSIA, SWE variants; first_seen 2022-05). "
    "C172 is active but exclusively scoped to BSITM — a different program family. "
    "AoS neighbors (D318, D329) confirm D-prefix usage in this guide. "
    "C172 is the BSITM-only variant; D315 is the correct code for BSCS/BSCSIA/BSIT."
),

# BSITM: C172 active 3CU exclusively in BSITM
"net_sec_found_c172": (
    "C172", "high", False, "program_name_fuzzy_match",
    "C172 is the active 3CU Network and Security - Foundations exclusively scoped to BSITM "
    "(current_programs: Bachelor of Science, Information Technology Management; perpetual stability). "
    "D315 is active but scoped to BSCNE/BSCSIA/SWE programs, not BSITM. "
    "C172's current_programs directly matches this BSITM guide."
),

# ------- IT: Fundamentals of Information Security -------
# BSCS: D430 active 3CU in BSCS/BSCS-to-MSCS; D827 active but BSCSIA-only; C836 inactive
"fund_infosec_bscs": (
    "D430", "high", False, "program_name_fuzzy_match",
    "D430 is the active 3CU Fundamentals of Information Security for BSCS programs "
    "(current_programs: Bachelor of Science, Computer Science; Bachelor of Science, Computer Science (BSCS to MSCS); first_seen 2023-02). "
    "D827 is active but exclusively scoped to BSCSIA — a different program. "
    "C836 is inactive with zero current_programs. "
    "D430 directly matches the BSCS program context."
),

# BSCSIA: D827 active 3CU in BSCSIA only
"fund_infosec_bscsia": (
    "D827", "high", False, "program_name_fuzzy_match",
    "D827 is the active 3CU Fundamentals of Information Security exclusively for BSCSIA programs "
    "(current_programs: Bachelor of Science, Cybersecurity and Information Assurance; first_seen 2025-07). "
    "D430 is active but scoped to BSCS programs, not BSCSIA. "
    "C836 is inactive with zero current_programs. "
    "D827 was introduced as a BSCSIA-specific replacement and directly matches this program."
),

# ------- IT: Introduction to IT -------
# BSCSIA: D322 active 4CU in BSCSIA explicitly
"intro_it_d322": (
    "D322", "high", False, "program_name_fuzzy_match",
    "D322 is the active 4CU Introduction to IT with current_programs that explicitly includes "
    "Bachelor of Science, Cybersecurity and Information Assurance (BSCSIA), as well as SWE and Cloud Computing. "
    "C182 is inactive with historical programs in business administration (not CS/IT), zero current_programs. "
    "E004 is active (3CU) but scoped to Cloud and Network Engineering programs, not BSCSIA. "
    "D322 directly matches the BSCSIA program context."
),

# BSIT: E004 inferred from AoS group cohort (E005/E006/E007 all E-prefix in same group)
"intro_it_e004": (
    "E004", "medium", True, "aos_group_neighbor_cohort",
    "E004 is the active 3CU Introduction to IT most consistent with the BSIT guide's IT Fundamentals AoS group. "
    "The three other resolved courses in the same AoS group (Business Productivity Software=E005, "
    "Digital Transformation in the Enterprise=E006, Agile Methodology=E007) all resolved to E-prefix codes, "
    "indicating the BSIT guide adopted the E-prefix cohort for this section. "
    "C182 is inactive with zero current_programs (historical in business admin). "
    "D322 is active (4CU) but scoped to BSCSIA/SWE — different from BSIT's general IT focus. "
    "E004 fits the E-prefix cohort; alternative D322 is possible given neither explicitly lists BSIT in current_programs."
),

# ------- IT: Technical Communication -------
# BSIT/MSIT/MSITM: E011 active 3CU with BSIT/MSIT/MSITM in current_programs
"tech_comm_e011": (
    "E011", "high", False, "program_name_fuzzy_match",
    "E011 is the active 3CU Technical Communication with current_programs that explicitly includes "
    "Bachelor of Science, Information Technology (BSIT to MSIT), Master of Science, Information Technology, "
    "and Master of Science, Information Technology Management (first_seen 2026-02). "
    "C768 and C948 are both inactive (C948 last_seen 2026-01, superseded by E011). "
    "D339 is active but scoped to BSCNE programs, not BSIT/MSIT/MSITM. "
    "E011's current_programs directly match this program context."
),

# ------- IT: Project Management -------
# BSITM: C722 active 3CU in broad business programs; AoS group neighbors all C-prefix (C715, C720, C721, C723)
"proj_mgmt_c722": (
    "C722", "high", False, "aos_group_neighbor_cohort",
    "C722 is the active 3CU Project Management in broad business/IT management programs "
    "(current_programs: 10 programs including BS Accounting, BS Business Management, Healthcare Admin; "
    "first_seen 2017-01, perpetual stability). "
    "AoS group neighbors for BSITM are all C-prefix codes (C715, C720, C721, C723), indicating this guide "
    "uses the C-prefix cohort for its management curriculum. "
    "C783 (4CU) is scoped to the BSIT-to-MSITM pathway program and MS Data Analytics — not standalone BSITM. "
    "E015 (4CU) was introduced in 2026-02 for the BSIT-to-MSIT pathway and MSIT, not standalone BSITM."
),

# MSIT: E015 active 4CU in MSIT explicitly
"proj_mgmt_e015": (
    "E015", "high", False, "program_name_fuzzy_match",
    "E015 is the active 4CU Project Management with current_programs that explicitly includes "
    "Master of Science, Information Technology and the BSIT to MSIT pathway (first_seen 2026-02). "
    "C722 (3CU) is scoped to broad business UG programs (Accounting, Business Management, etc.) — not IT graduate. "
    "C783 (4CU) is scoped to MS Data Analytics - Decision Process Engineering and the BSIT-to-MSITM pathway, "
    "not standalone MSIT. E015 directly matches the MSIT program context."
),

# ------- Business: Fundamentals for Success in Business -------
# D072 active 3CU (6 programs); C994 inactive legacy (last_seen 2020-01); D072A cert-only
"fund_success_biz": (
    "D072", "high", False, "legacy_vs_active_code_pattern",
    "D072 is the active 3CU Fundamentals for Success in Business (current_programs: 6 programs including "
    "BS Accounting, Finance, Healthcare Administration; first_seen 2020-02). "
    "C994 is the superseded predecessor code (last_seen 2020-01, zero current_programs) — "
    "discontinued when D072 was introduced. "
    "D072A has cert_only stability (Business Leadership certificate program) — not applicable to a degree guide. "
    "D072 directly replaces C994 for degree programs via the legacy-vs-active pattern."
),

# ------- Health: Health Equity and Social Determinants -------
# BSHS/BSPH/BSPSY: both D057 and D397 inactive, different discontinued programs
"health_equity_unresolvable": (
    None, "unresolvable", False, "other",
    None,  # unresolvable_reason provided separately
),

# ------- Nursing UG: Emerging Professional Practice -------
# BSNU: E225 active 3CU in BS Nursing (current); D225 now scoped to MSN RN-to-MSN
"emerg_prof_prac_e225": (
    "E225", "high", False, "program_name_fuzzy_match",
    "E225 is the active 3CU Emerging Professional Practice exclusively scoped to Bachelor of Science, Nursing "
    "(current_programs: Bachelor of Science, Nursing; first_seen 2024-08). "
    "D225 was historically in the BSN program but is now scoped to MSN RN-to-MSN programs only "
    "(current_programs: MSN Education, Leadership, Management RN to MSN programs). "
    "E225 was introduced in 2024-08 as the current BSNU code, directly replacing D225 for the BSN context."
),

# MSRNN*: D225 active 3CU in MSN RN-to-MSN programs (3 programs)
"emerg_prof_prac_d225": (
    "D225", "high", False, "program_name_fuzzy_match",
    "D225 is the active 3CU Emerging Professional Practice for MSN RN-to-MSN programs "
    "(current_programs: Master of Science, Nursing - Education (RN to MSN); Leadership and Management (RN to MSN); "
    "Informatics (RN to MSN); first_seen 2022-01). "
    "E225 is active but exclusively scoped to the undergraduate BSN program (Bachelor of Science, Nursing). "
    "This guide is an MSN RN-to-MSN program; D225 directly matches."
),

# ------- Nursing UG: Global and Population Health -------
# BSNU: E224 active 4CU in BS Nursing only
"global_pop_health_e224": (
    "E224", "high", False, "program_name_fuzzy_match",
    "E224 is the active 4CU Global and Population Health exclusively scoped to Bachelor of Science, Nursing "
    "(current_programs: Bachelor of Science, Nursing; first_seen 2024-08). "
    "D224 was historically in the BSN program but is now scoped to MSN RN-to-MSN programs only. "
    "E224 was introduced in 2024-08 as the current BSNU code, replacing D224 for the BSN context."
),

# MSRNN*: D224 active 4CU in MSN RN-to-MSN programs
"global_pop_health_d224": (
    "D224", "high", False, "program_name_fuzzy_match",
    "D224 is the active 4CU Global and Population Health for MSN RN-to-MSN programs "
    "(current_programs: MSN Education, Leadership and Management, Informatics RN to MSN; first_seen 2022-01). "
    "E224 is active but exclusively scoped to the undergraduate BSN program. "
    "This guide is an MSN RN-to-MSN program; D224 directly matches."
),

# ------- Nursing: Pathophysiology -------
# BSPRN/MSRNN*: D236 active 3CU in nursing programs (6 programs incl Nursing, Nursing-Prelicensure)
"pathophys_d236": (
    "D236", "high", False, "program_name_fuzzy_match",
    "D236 is the active 3CU Pathophysiology for nursing programs "
    "(current_programs: 6 programs including Bachelor of Science, Nursing; Bachelor of Science, Nursing - Prelicensure; "
    "first_seen 2022-01). "
    "C805 is active but scoped to Health Information Management — a different program domain. "
    "D069 is inactive (zero current_programs, last_seen 2022-11, historically in BS Health Services Coordination). "
    "D236 directly matches nursing program contexts including prelicensure."
),

# ------- Nursing BSPRN: Community Health -------
# C826 hist=BSRN (pre-licensure); C228 hist=BSNU+MSN (post-licensure/graduate)
"comm_health_c826": (
    "C826", "medium", True, "program_name_fuzzy_match",
    "C826 (inactive, last_seen 2022-12) was historically scoped to Bachelor of Science, Nursing [BSRN], "
    "a pre-licensure nursing program analogous to BSPRN (Bachelor of Science, Nursing - Prelicensure). "
    "C228 (inactive, last_seen 2021-12) was historically scoped to BSNU (post-licensure BSN) and MSN RN-to-MSN "
    "programs — a different clinical context from pre-licensure nursing. "
    "Both candidates are now inactive with no current programs; the active D-prefix replacement is resolved elsewhere. "
    "C826's BSRN scope is the closer semantic match to BSPRN, but C228 cannot be fully excluded "
    "since both served nursing programs and BSPRN students may follow a curriculum that historically drew from BSNU."
),
}  # end R dict

UNRESOLVABLE_REASONS = {
    "health_equity_unresolvable": (
        "Both candidates are inactive with zero current_programs. D057 (last_seen 2022-11) was historically "
        "in Bachelor of Science, Health Services Coordination. D397 (last_seen 2024-09) was historically in "
        "Bachelor of Science, Health and Human Services. Neither historical program matches the current guide's "
        "program family (Health Science, Public Health, or Psychology). No available signal — "
        "AoS neighbors resolve to unrelated D-prefix codes (career/psychology), sp_cus is non-unique, "
        "and both candidates have identical structure (3CU, moderate stability, inactive, same college implied)."
    ),
}


# ---------------------------------------------------------------------------
# Build packet → decision mapping
# ---------------------------------------------------------------------------

def make_result(packet_id, decision_key, *, override_code=None, override_review=False):
    code, conf, alt, signal, rationale = R[decision_key]
    if override_code is not None:
        code = override_code
    unres_reason = UNRESOLVABLE_REASONS.get(decision_key) if conf == "unresolvable" else None
    return {
        "packet_id": packet_id,
        "selected_code": code,
        "confidence": conf,
        "alternative_possible": alt,
        "rationale": rationale,
        "signal_used": signal,
        "unresolvable_reason": unres_reason,
        "review_flag": override_review or (conf == "unresolvable"),
    }


def build_all_results():
    # Load packets to get ordered list
    with open(PACKETS_IN) as f:
        data = json.load(f)
    packets = data["packets"]

    results = []

    for p in packets:
        pid = p["packet_id"]
        pc = p["program_context"]
        prog = pc["program_code"]
        family = pc["family"]
        level = pc["degree_level"]
        rc = p["row_context"]
        title_norm = rc["guide_title_normalized"]

        # ---- EDUCATION BA / BS / TEACHING_MAT ----

        if title_norm == "elementary disciplinary literacy":
            if family == "teaching_mat":
                results.append(make_result(pid, "elem_disc_lit_mat"))
            else:
                results.append(make_result(pid, "elem_disc_lit_ug"))

        elif title_norm == "elementary social studies methods":
            results.append(make_result(pid, "elem_soc_studies_ug"))

        elif title_norm == "student teaching i in elementary education":
            if family == "teaching_mat":
                results.append(make_result(pid, "st1_elem_mat"))
            else:
                results.append(make_result(pid, "st1_elem_ug"))

        elif title_norm == "student teaching ii in elementary education":
            if family == "teaching_mat":
                results.append(make_result(pid, "st2_elem_mat"))
            else:
                results.append(make_result(pid, "st2_elem_ug"))

        elif title_norm == "student teaching i in special education":
            if family == "teaching_mat":
                results.append(make_result(pid, "st1_sped_mat"))
            else:
                results.append(make_result(pid, "st1_sped_ug"))

        elif title_norm == "student teaching ii in special education":
            if family == "teaching_mat":
                results.append(make_result(pid, "st2_sped_mat"))
            else:
                results.append(make_result(pid, "st2_sped_ug"))

        elif title_norm == "secondary disciplinary literacy":
            if family == "teaching_mat":
                results.append(make_result(pid, "sec_disc_lit_mat"))
            else:
                results.append(make_result(pid, "sec_disc_lit_ug"))

        elif title_norm == "student teaching i in secondary education":
            if family == "teaching_mat":
                results.append(make_result(pid, "st1_sec_mat"))
            else:
                results.append(make_result(pid, "st1_sec_ug"))

        elif title_norm == "student teaching ii in secondary education":
            if family == "teaching_mat":
                results.append(make_result(pid, "st2_sec_mat"))
            else:
                results.append(make_result(pid, "st2_sec_ug"))

        elif title_norm == "advanced calculus":
            results.append(make_result(pid, "adv_calc_ug"))

        elif title_norm == "algebra for secondary mathematics teaching":
            if family == "teaching_mat":
                results.append(make_result(pid, "alg_sec_math_mat"))
            else:
                results.append(make_result(pid, "alg_sec_math_ug"))

        elif title_norm == "calculus i":
            results.append(make_result(pid, "calc1_ug"))

        elif title_norm == "calculus ii":
            results.append(make_result(pid, "calc2_ug"))

        elif title_norm == "linear algebra":
            results.append(make_result(pid, "lin_alg_ug"))

        elif title_norm == "general chemistry ii with lab":
            results.append(make_result(pid, "gen_chem2_ug"))

        elif title_norm == "organic chemistry":
            results.append(make_result(pid, "org_chem_ug"))

        elif title_norm == "astronomy":
            results.append(make_result(pid, "astronomy_ug"))

        # ---- CS / IT ----

        elif title_norm == "business of it applications":
            if prog == "BSITM":
                results.append(make_result(pid, "biz_it_apps_c179"))
            else:
                results.append(make_result(pid, "biz_it_apps_d336"))

        elif title_norm == "data management foundations":
            if prog == "BSITM":
                results.append(make_result(pid, "data_mgmt_c175"))
            else:
                results.append(make_result(pid, "data_mgmt_d426"))

        elif title_norm == "network and security foundations":
            if prog == "BSITM":
                results.append(make_result(pid, "net_sec_found_c172"))
            else:
                results.append(make_result(pid, "net_sec_found_d315"))

        elif title_norm == "fundamentals of information security":
            if prog == "BSCSIA":
                results.append(make_result(pid, "fund_infosec_bscsia"))
            else:  # BSCS
                results.append(make_result(pid, "fund_infosec_bscs"))

        elif title_norm == "introduction to it":
            if prog == "BSCSIA":
                results.append(make_result(pid, "intro_it_d322"))
            else:  # BSIT
                results.append(make_result(pid, "intro_it_e004"))

        elif title_norm == "technical communication":
            results.append(make_result(pid, "tech_comm_e011"))

        elif title_norm == "project management":
            if prog == "BSITM":
                results.append(make_result(pid, "proj_mgmt_c722"))
            else:  # MSIT
                results.append(make_result(pid, "proj_mgmt_e015"))

        elif title_norm == "fundamentals for success in business":
            results.append(make_result(pid, "fund_success_biz"))

        # ---- HEALTH ----

        elif title_norm == "health equity and social determinants of health":
            results.append(make_result(pid, "health_equity_unresolvable", override_review=True))

        # ---- NURSING ----

        elif title_norm == "emerging professional practice":
            if family == "nursing_ug":  # BSNU
                results.append(make_result(pid, "emerg_prof_prac_e225"))
            else:  # nursing_rn_msn (MSRNN*)
                results.append(make_result(pid, "emerg_prof_prac_d225"))

        elif title_norm == "global and population health":
            if family == "nursing_ug":  # BSNU
                results.append(make_result(pid, "global_pop_health_e224"))
            else:  # MSRNN*
                results.append(make_result(pid, "global_pop_health_d224"))

        elif title_norm == "pathophysiology":
            results.append(make_result(pid, "pathophys_d236"))

        elif title_norm == "community health and population focused nursing":
            results.append(make_result(pid, "comm_health_c826"))

        else:
            raise ValueError(f"Unhandled title_norm: {title_norm!r} in packet {pid}")

    return results


def main():
    results = build_all_results()

    # Stats
    by_conf = {}
    for r in results:
        by_conf[r["confidence"]] = by_conf.get(r["confidence"], 0) + 1
    auto_accept = sum(1 for r in results if r["confidence"] == "high" and not r["alternative_possible"])
    spot_check = sum(1 for r in results if r["confidence"] == "high" and r["alternative_possible"])
    human_review = sum(1 for r in results if r["confidence"] == "medium")
    unresolvable = sum(1 for r in results if r["confidence"] == "unresolvable")

    output = {
        "generated_on": str(date.today()),
        "adjudicator": "llm_claude_sonnet_4_6",
        "total_adjudications": len(results),
        "summary": {
            "high_no_alt_auto_accept": auto_accept,
            "high_alt_spot_check": spot_check,
            "medium_human_review": human_review,
            "unresolvable": unresolvable,
        },
        "adjudications": results,
    }

    with open(RESULTS_OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print("LLM ADJUDICATION RESULTS — WRITTEN")
    print("=" * 60)
    print(f"  Total adjudications: {len(results)}")
    print(f"  High, auto-accept:   {auto_accept}")
    print(f"  High, spot-check:    {spot_check}")
    print(f"  Medium, review:      {human_review}")
    print(f"  Unresolvable:        {unresolvable}")
    print(f"  Net accepted (high): {auto_accept + spot_check}")
    print(f"  Output: {RESULTS_OUT}")
    print("=" * 60)


if __name__ == "__main__":
    main()
