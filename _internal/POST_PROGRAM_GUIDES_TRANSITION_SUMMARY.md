# Post-Program-Guides Transition Summary

**Date:** 2026-03-21
**Purpose:** Document the transition from program guides completion to the new three-track direction

## What Was Accomplished

### Documentation Updates
Successfully updated the core repository documentation to reflect the new post-program-guides direction:

1. **`_internal/ATLAS_CONTROL.md`**
   - Added new workstream rows for Degrees, Courses, and Homepage
   - Updated program guide extraction status to reflect completion
   - Maintained existing workstream structure while adding new direction

2. **`_internal/ATLAS_REPO_MEMORY.md`**
   - Added explicit post-program-guides direction under Product-level decisions
   - Encoded the three-track focus as durable repo memory

3. **`_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md`**
   - Added "Post-program-guides direction" section
   - Maintained all existing technical status while adding strategic context

4. **`data/program_guides/README.md`**
   - Updated main human entry point with new direction
   - Preserved all technical documentation while adding strategic framing

## New Project Direction

### Three-Track Focus

1. **Degrees** (Immediate Implementation Target)
   - Leverage completed guide data (751 enriched courses)
   - Build Atlas degree-enrichment artifact generator
   - First surface to strengthen with guide-derived content

2. **Courses** (Major Follow-On Opportunity)
   - 751 canonical courses have guide-derived enrichment candidates
   - Course-page enrichment strategy to be designed
   - Sequenced after degree page implementation

3. **Homepage** (Presentation Layer)
   - Redesign to showcase stronger degree and course understanding
   - Sequenced after inner-surface strengthening
   - Proof surface for enhanced product value

### Key Constraints Maintained

- **Guide data is complete as a data asset** but not yet live on the site
- **Course enrichment is important but not immediate** - comes after degrees
- **Homepage redesign follows inner-surface work** - not the first move
- **No overclaiming of current site integration** - maintains accuracy

## Current Status

### Program Guides: ✅ COMPLETE
- 115/115 guidebooks collected, parsed, and validated
- 751 canonical courses with guide-derived enrichment
- Policy and schema for degree-enrichment designed
- Artifact generator not yet built

### Next Implementation Step
**Build the Atlas degree-enrichment artifact generator** (`build_guide_artifacts.py`):
- Reads extracted guide data
- Applies approved inclusion policy
- Emits Atlas-ready JSON for degree pages
- No site wiring yet - produces files for verification

## Strategic Benefits

1. **Clear Direction**: Project now has explicit three-track focus instead of vague "finish program guides"
2. **Leverages Completed Work**: Uses the substantial program guide investment as foundation
3. **Sequenced Implementation**: Logical progression from degrees → courses → homepage
4. **Maintains Quality**: Preserves all existing cautions and accuracy requirements
5. **Product-Focused**: Centers on user-facing value rather than internal pipeline work

## Next Actions

1. **Immediate**: Build degree-enrichment artifact generator using existing policy/schema
2. **Short-term**: Design course-page enrichment strategy leveraging 751 enriched courses
3. **Medium-term**: Plan homepage redesign based on strengthened inner surfaces
4. **Ongoing**: Continue official resource layer work in parallel

## Files Modified

- `_internal/ATLAS_CONTROL.md` - Active control surface updated
- `_internal/ATLAS_REPO_MEMORY.md` - Stable repo memory updated  
- `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md` - Module status updated
- `data/program_guides/README.md` - Human entry point updated

## Maintained Documentation Standards

- **Factual accuracy**: No overclaiming of current site integration
- **Clear sequencing**: Explicit order of implementation priorities
- **Technical precision**: Maintained all existing technical details
- **Strategic clarity**: Clear three-track direction without ambiguity