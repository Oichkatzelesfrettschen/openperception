# Motion Token From Foundations

Date: 2026-03-22

## What `motion.json` really is

`specs/tokens/temporal/motion.json` is the repo's temporal-safety token
contract.

It translates seizure safety, motion sensitivity, and frame-rate independence
into structured token data for:

- durations,
- frequency caps,
- pulse limits,
- luminance modulation,
- easing families,
- display-mode overrides.

So this is one of the clearest machine-readable expressions of the repo's
temporal accessibility ambitions.

## Step 1. What it gets especially right

The strongest move here is that everything is defined in time, not frames.

That matches the larger repo logic perfectly:

- refresh rate is a device property,
- content timing is an authoring responsibility,
- safety constraints must not depend on frame count assumptions.

## Step 2. Why this file matters

This token file shows how the temporal spec family could eventually become
enforceable:

- hard caps become tokenized limits,
- display profiles become structured overrides,
- unsafe easing patterns are named explicitly.

That is exactly the kind of contract needed before a validator or renderer can
do meaningful work.

## Step 3. What remains aspirational

Like several neighboring token specs, this file is ahead of current runtime
implementation.

The repo does not yet have a broad motion-token engine or validator that
enforces this temporal contract across products.

So the file is best read as a future control surface rather than a presently
wired system.

## Bottom line

`specs/tokens/temporal/motion.json` is the repo's temporal-safety token
contract. It is a strong example of how OpenPerception wants to turn motion and
seizure guidance into structured, machine-consumable policy, even though that
policy is not yet broadly enforced.
