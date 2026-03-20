# Continuity Review Method Plan

## 1. What continuity review is for

A continuity review method inside Atlas serves as a **bounded evaluation gate** that helps the team decide:
- Whether degree continuity deserves more product weight in the roadmap
- What a lightweight continuity surface could look like
- Whether course continuity is worth pursuing later

It is **not** a full implementation of continuity features, but rather a **review and decision-making framework** that enables quick, human-centered evaluation of continuity cases before committing to larger development efforts.

The review method should be **fast, discussable, and decision-oriented**, providing enough context for stakeholders to make informed choices about product direction without getting bogged down in heavy UI development or complex system building.

## 2. Minimum viable review format options

### Compact text cards (Recommended)

**What it shows:**
- Event type (successor, split, family restructure, etc.)
- From-program(s) and to-program(s) with codes and names
- Key metrics: Jaccard overlap, shared/added/removed course counts
- Decision status (approved, pending, excluded)
- Change summary template (for approved events)
- Any special notes (zero overlap rationale, wording guard, gap check)

**What it hides:**
- Full course lists (show only counts)
- Complex lineage graphs
- Historical timeline details
- Implementation complexity details

**Why it's useful for review:**
- **Human-readable**: Easy to scan and discuss in meetings
- **Compact**: Fits on a single page or slide
- **Decision-focused**: Clearly shows what needs approval
- **Context-rich**: Provides enough data for informed decisions without overwhelming detail

### Visual/diagram option (Secondary)

**What it shows:**
- Simple flow diagrams showing program relationships
- Overlap percentages as visual indicators
- Timeline markers for edition boundaries

**What it hides:**
- Detailed course mappings
- Complex multi-program relationships
- Technical implementation details

**Why it's useful:**
- **Visual learners**: Helps understand relationships at a glance
- **Presentation-friendly**: Good for stakeholder meetings
- **Pattern recognition**: Easier to spot trends across multiple events

### Comparison table format (Alternative)

**What it shows:**
- Side-by-side comparison of key metrics
- Decision status columns
- Priority indicators

**What it hides:**
- Narrative context
- Qualitative assessments
- Detailed reasoning

**Why it's useful:**
- **Data-focused**: Good for analytical review
- **Comparative**: Easy to rank and prioritize
- **Structured**: Consistent format across reviews

## 3. Recommended first format

**Compact text cards** are the best first method because they:
- Provide the right balance of detail and brevity
- Are easily created and shared without specialized tools
- Support both individual review and group discussion
- Can be enhanced with visual elements later if needed
- Align with the project's emphasis on low-maintenance, reproducible workflows

## 4. Proposed validation batch size

**Recommendation: 4 review cards** covering the four pattern types:
- 1 clean successor (high overlap, clear progression)
- 1 rebuilt replacement (low overlap, substantial change)
- 1 split family (one-to-many relationship)
- 1 ambiguous case (pending HITL decision)

**Why this size:**
- **Minimal viable**: Tests the format without overcommitting
- **Pattern coverage**: Ensures the method works for different relationship types
- **Quick validation**: Can be reviewed and refined in a single session
- **Scalable foundation**: Provides template for larger batches later
- **Risk mitigation**: Avoids building extensive artifacts before validating the approach

## 5. Candidate example classes

### Clean successor
**Candidate:** PLE-001 (BSITSEC → BSNOS)
- **Why:** High Jaccard overlap (0.769), clear progression, no special considerations
- **Value:** Establishes baseline for straightforward cases

### Rebuilt replacement
**Candidate:** PLE-011 (BSNOS → BSNES)
- **Why:** Low overlap (0.043), substantial curriculum change, wording guard required
- **Value:** Tests handling of major program transformations

### Split family
**Candidate:** PLE-010 (BSCC → BSCCMCL, BSCCAWS, BSCCAZR)
- **Why:** One-to-many relationship, multiple vendor tracks, strategic shift
- **Value:** Tests handling of complex program restructuring

### Ambiguous case
**Candidate:** PLE-012 (BSHSC → BSHHS)
- **Why:** Pending HITL decision, requires health curriculum expert confirmation
- **Value:** Tests handling of uncertain cases and decision documentation

## 6. What this module should not become

### Failure modes to avoid:
- **Turning into a giant internal history project**: Don't build comprehensive historical archives without clear student value
- **Building a full viewer-facing feature too early**: Avoid heavy UI development before validating the concept
- **Reviewing too many weak cases**: Focus on clear, impactful continuity relationships first
- **Getting bogged down in edge cases**: Don't let ambiguous cases derail the main review process
- **Creating maintenance-heavy systems**: Keep the review method lightweight and sustainable
- **Losing sight of current student navigation**: Remember that continuity is supporting context, not the main product identity

### Boundaries to maintain:
- **Bounded scope**: Review only what's necessary for product decisions
- **Student-first focus**: Always tie back to current student value
- **Low maintenance**: Use existing tools and workflows
- **Decision-oriented**: Focus on enabling choices, not creating artifacts

## 7. Single best next bounded task

**Create the first validation batch of 4 review cards** using the compact text card format, covering the four pattern types identified above. This will:

1. **Validate the format**: Test whether the card structure provides the right level of detail
2. **Enable stakeholder review**: Give the team concrete artifacts to evaluate
3. **Establish the workflow**: Create a repeatable process for future reviews
4. **Inform product decisions**: Provide the basis for deciding whether to invest in continuity features

The output should be a single markdown document containing all 4 review cards, ready for team discussion and decision-making.

This approach aligns with the project's emphasis on **low-cost, high-value review methods** and provides a clear path forward without overcommitting to heavy development work.