# RPS strategy brief: quantitative model

**Conventions**
- **Edge** is P(win) − P(loss) per throw, in percentage points (pp).
- **q** is P(win | decisive throw). Ties are always replayed.
- **X** is the opponent's previous hand. **X+** is the hand that beats X (Rock → Paper). **X−** is the hand X beats (Rock → Scissors).
- **Opponent state W/T/L** is the opponent's own previous outcome. W means they won, which means we lost.
- **Rule notation "a/b/c"** gives our throw after the opponent's win / tie / loss.
- **"Upper bound"** means the opponent behaves exactly like the population-average table and does not adapt.

---

## Key numbers the synthesis should quote

| # | Number | Source of parameters |
|---|---|---|
| K1 | **First-throw base rates.** Paper nets +2.8 pp [95% CI +2.7, +2.9] against 5.0M online openers. Experienced players' openers favour Scissors instead (+2.0 [+1.8, +2.1]; Paper −0.2). An edge on the first throw only adds just 0.25×e1 to a Bo3 match: +2.8 pp becomes 50.7%. | baserates:C01 |
| K2 | **All-throw Rock excess.** Always throwing Paper nets +2.8 to +4.9 pp in 9 datasets: Zhejiang labs, Western labs, AU pairs, JP live hands and the Batzilis proxy. It nets −2.7 [−4.8, −0.7] in US dyads and −2.0 in UK live play. Hungarian live play had a Scissors excess (36.8%). | C04, A4, B1, C18, MF03, C05, C11 |
| K3 | **Being watched matters more than base rates.** If your visible openers are ≥42% Rock, opponents open Paper 46.6%, so Scissors nets **+16.2 pp**. If your Rock share is 0–25%, Rock nets +10.0. | sequential:D1, foundations:C18 |
| K4 | **Upper bound from exploiting the opponent's conditional pattern** (best response to its own population, long run). Zhejiang a=2: +17.2 pp/throw, Bo3 0.659. Western labs: +10.9 to +13.4, Bo3 0.59–0.61. US/AU fixed pairs: +8.2 / +6.9, Bo3 0.567 / 0.564. Halving the opponent's biases roughly halves these. If only the after-loss bias exists: +1.9 to +6.3 pp, Bo3 0.514–0.544. | A1, C2, B1, B2, MF5, C1 |
| K5 | **The best response flips sign between populations.** The Zhejiang best response loses 6.4 pp/throw against AU pairs. "Always X−" (the US/AU best response) loses 18.7 pp/throw against Zhejiang a=2. | A1, C1, C2 |
| K6 | **Only one robust per-state rule.** Of 63 per-state rules (each state: X+, X, X− or random; all-random excluded), only **X+/X−/X−** is non-negative against all 7 full-session tables. Its minimum is +0.4, mean +7.0 (West +8.5, Zhejiang +3.2). In rounds 1–20 it scores −0.3 [−3.8, +3.3] (US), +1.7 (AU) and +3.1 (ZJ). Bo3 ranges 0.498–0.610. In words: if they just won, beat their hand; otherwise throw the hand their last hand beats. In your own terms: after a loss or tie, throw the hand your last hand beats; after a win, throw the hand that beats your last hand. | all conditional tables |
| K7 | **After a tie.** In fixed-opponent and Western data, X− wins: +5.4 [+1.2, +9.7] AU and +5.8 [+2.4, +9.1] US (Rock–Rock → Scissors), and +8.0 to +12.6 in Western labs. In Zhejiang data X+ wins: +19.8 at a=2, shrinking to +5.5 when a tie pays nothing (a=∞). In rounds 1–20 no response is distinguishable from 0 (CI ±6–9 pp). | MF01, B1, B2, A1, C08, MF02, MF2 |
| K8 | **Format amplification.** At q=0.55: Bo3 0.575, Bo5 0.593, 5-a-side relay 0.621, 7-a-side relay 0.644, 5-member points format with Bo3 bouts 0.638. Realistic edges are small: experienced online players' realised +1.49 pp gives q=0.511 and Bo3 0.516. | team:C3, C9, foundations:C16 |
| K9 | **Host game: coordinated even split is exactly optimal.** Rule A (only winners survive), n=10, k=2: 0.692 → 1.000. Rule A, n=20, k=3: 0.530 → 0.741. Rule B (ties also survive), n=10, k=5: 0.756 → 0.959. Herding gives (1/3)^k or (2/3)^k. | team:C7 |
| K10 | **Our exploitability.** A deterministic rule gives Bo3 P(win) = 0.000 against an opponent who knows it. Following a rule with probability p costs exactly −p per throw (Bo3 0.168 at p=0.5). In 300-round sessions humans recovered about 50% of the theoretical maximum against simple transition bots and 14–18% against outcome-conditioned bots. The task's example rule ("beat the previous winning hand") is the 14% type. | sequential:D4, MF1 |
| K11 | **P(simultaneous n-player round is decisive)** = 3(2^n−2)/3^n: 0.667 (n=2–3), 0.370 (n=5), 0.052 (n=10). | team:C4 |
| K12 | **Simultaneous 3v3 team throw.** Composition "2 on X + 1 on the hand X beats" wins 11/16 = 0.6875 (rule I) and 175/256 = 0.684 (rule II) against an independent team. The reverse orientation gives 0.3125 / 0.469. | team:C6/MF1 |
| K13 | **Relay challenger lean** (throw the hand that beats the champion's last winning hand) gives +7.3 pp on that throw, using the Western new-opponent win-stay of 38.2%. Against Zhejiang-like champions it gives +28.1. Effect on a 5-a-side relay: 0.540 / 0.520 (single-throw / Bo3 bouts) or 0.652 / 0.577. | sequential:B4, team:C15, A1 |

---

## 1. First throw and marginal base rates

The W/T/L of a throw is (share of the hand it beats / same hand / hand that beats it). "Adj. CI" inflates the naive multinomial CI by √(1+(m−1)ρ), with ρ = 0.0166 and m = throws per player (see Assumptions).

| Opponent distribution [source] | n | Opp R/P/S % | Edge R / P / S | Best throw: W/T/L %; edge [naive 95% CI] | Adj. CI |
|---|---|---|---|---|---|
| Online first throws, all (2007) [C01] | 5,012,128 | 33.99/34.82/31.20 | −3.6 / +2.8 / +0.8 | P 34.0/34.8/31.2; +2.8 [+2.7, +2.9] | [+2.7, +2.9] |
| Online first throws, experienced [C01] | 1,472,319 | 32.60/34.56/32.84 | −1.7 / −0.2 / +2.0 | S 34.6/32.8/32.6; +2.0 [+1.8, +2.1] | [+1.7, +2.2] |
| Openers vs a player whose shown history is ≥42% Rock [D1/C18] | 1,056,162 | 30.35/46.58/23.06 | −23.5 / +7.3 / +16.2 | S 46.6/23.1/30.4; +16.2 [+16.1, +16.4] | – |
| Openers vs a player whose shown history is 0–25% Rock [D1/C18] | 1,006,726 | 35.84/27.07/37.09 | +10.0 / −1.3 / −8.8 | R 37.1/35.8/27.1; +10.0 [+9.9, +10.2] | – |
| Eyler novices vs computer [C02] | 119 | 55.5/32.8/11.8 | −21.0 / +43.7 / −22.7 | P 55.5/32.8/11.8; +43.7 [+31.2, +56.2] | – |
| US dyads, round 1 [MF04] | 120 | 33.3/44.2/22.5 | −21.7 / +10.8 / +10.8 | S 44.2/22.5/33.3; +10.8 [−4.8, +26.5] (P same edge, [−2.4, +24.1]) | – |
| AU pairs, game 1 [MF04] | 49 | 28.6/24.5/46.9 | +22.4 / −18.4 / −4.1 | R 46.9/28.6/24.5; +22.4 [−0.4, +45.3] | – |
| JP survey, STATED opener [C14] | 1,000 | 37.4/20.6/42.0 | +21.4 / −4.6 / −16.8 | R 42.0/37.4/20.6; +21.4 [+16.7, +26.1] | – |
| … men (stated) | 337 | 42.4/25.2/32.3 | +7.1 / +10.1 / −17.2 | P 42.4/25.2/32.3; +10.1 [+0.9, +19.3] | – |
| … women (stated) | 663 | 34.8/18.3/46.9 | +28.7 / −12.1 / −16.6 | R 46.9/34.8/18.3; +28.7 [+22.9, +34.4] | – |
| Online all-throw proxy [C01] | – | 35.45/34.01/30.54 | −3.5 / +4.9 / −1.4 | P 35.5/34.0/30.5; +4.9 (no n) | – |
| Zhejiang lab a=2 (Xu 2013) [C04] | 21,600 | 35.7/32.1/32.2 | +0.1 / +3.4 / −3.5 | P 35.7/32.1/32.2; +3.4 [+2.3, +4.5] | [+0.8, +6.1] |
| Zhejiang, 354 players (overlaps Xu) [A4] | 354 pl. | 36/33/32 | −1.0 / +4.0 / −3.0 | P 36/33/32; +4.0 [+2.5, +5.5] (player SDs, worst-case covariance) | – |
| Zhejiang vs AI (Wang L 2020) [C04] | 12,300 | 35.5/32.1/32.4 | +0.3 / +3.2 / −3.4 | P 35.5/32.1/32.4; +3.2 [+1.7, +4.6] | [−0.4, +6.7] |
| Canada vs computer (Dyson 2016) [B1] | 6,975 | 35.6/32.2/32.2 | −0.1 / +3.4 / −3.4 | P 35.6/32.2/32.2; +3.4 [+1.5, +5.4] | [−0.8, +7.6] |
| UK vs computer (Forder & Dyson) [C18] | 16,200 | 35.2/32.5/32.4 | −0.1 / +2.8 / −2.7 | P 35.2/32.5/32.4; +2.8 [+1.5, +4.1] | [−0.9, +6.5] |
| Canada vs computer (Dyson 2022) [MF03] | ~14,400 | 35.8/32.8/31.4 | −1.5 / +4.4 / −3.0 | P 35.8/32.8/31.4; +4.4 [+3.1, +5.8] | [+0.9, +8.0] |
| AU fixed pairs (Moerel) [C12/MF03] | 29,511 | 35.3/32.5/32.1 | −0.4 / +3.2 / −2.8 | P 35.3/32.5/32.1; +3.2 [+2.3, +4.2] | **[+1.4, +5.2]** (reported cluster bootstrap) |
| US fixed dyads (Brockbank & Vul) [MF03] | 35,969 | 31.9/33.6/34.6 | +1.0 / **−2.7** / +1.7 | S 33.6/34.6/31.9; +1.7 [+0.9, +2.5] | [−0.3, +3.7]; Paper −2.7 **[−4.8, −0.7]** (reported) |
| UK live hands (Cook) [C11] | ~5,040 | 32.4/33.3/34.4 | +1.1 / −2.0 / +0.9 | R 34.4/32.4/33.3; +1.1 [−1.2, +3.4] | [−4.9, +7.1] |
| HU live hands (Aczel) [C11] | – | S 36.8; R and P not reported | if R=P: +5.1 / −5.1 / 0 | R (assumption-based) | – |
| JP live hands (Yoshizawa) [C05] | 11,567 | 35.0/33.3/31.7 | −1.6 / +3.4 / −1.8 | P 35.0/33.3/31.7; +3.4 [+1.9, +4.9] | [+1.7, +5.0] |
| TV sequence, anecdotal (Sazae-san) [C16] | 1,347 | 32.4/33.0/34.7 | +1.7 / −2.3 / +0.6 | R 34.7/32.4/33.0; +1.7 [−2.7, +6.1] | – |

**Reading the table**
- Population edges from marginal frequencies are at most about 3–5 pp, and their sign depends on the population.
- Opening-throw samples of n≈50–120 swing ±20 pp, so their CIs span zero or nearly so.
- The large effect is reactive: opponents respond to what they have seen you throw (K3).

---

## 2. Conditional exploitation (Markov chain)

**2a. Best response to each opponent table, stationary edge and match outcomes.** The first throw of each match is random for both players.

| Opponent table [source] | After opp W | After tie | After opp L | Stationary edge/throw (tie %) | q | Bo3 P(win) (edge/throw in Bo3) | Bo5 | Biases ×0.5: edge, Bo3 | Only after-loss bias: edge, Bo3 |
|---|---|---|---|---|---|---|---|---|---|
| Zhejiang a=2, random re-matching [A1] | X+ +28.1 | X+ +19.8 | X +8.9 | **+17.2** (31.7) | 0.626 | **0.659** (+13.5) | 0.715 | +9.0, 0.582 | +3.1, 0.522 |
| Zhejiang vs AI [C2] | X+ +22.1 | X+ +9.1 | X+ +7.0 | +12.0 (30.4) | 0.586 | 0.603 (+8.7) | 0.645 | +6.2, 0.552 | +2.4, 0.517 |
| Canada vs computer (Dyson 2016) [B1] | X +2.9 | X− +12.6 | X− +14.9 | +10.9 (36.3) | 0.586 | 0.595 (+8.0) | 0.630 | +5.3, 0.547 | +5.2, 0.537 |
| UK vs computer (Forder & Dyson) [B2] | X+ +14.2 | X− +8.0 | X− +17.7 | +13.4 (34.7) | 0.603 | 0.610 (+9.1) | 0.656 | +6.7, 0.555 | +6.3, 0.544 |
| Canada vs computer (Dyson 2021 Exp 1) [MF5] | X+ +8.1 | X− +8.6 | X− +15.1 | +10.9 (34.8) | 0.584 | 0.591 (+7.6) | 0.628 | +5.4, 0.545 | +5.3, 0.538 |
| US fixed dyads [C1] | X− +3.6 | X− +5.8 | X− +14.0 | +8.2 (35.6) | 0.563 | 0.567 (+5.5) | 0.595 | +4.0, 0.533 | +4.9, 0.535 |
| AU fixed pairs [C1] | X− +10.3 | X− +5.6 | X− +5.5 | +6.9 (37.7) | 0.555 | 0.564 (+5.0) | 0.590 | +3.5, 0.531 | +1.9, 0.514 |
| US rounds 1–20 [MF2] | X− +10.2 [+4.4, +16.0] | X +1.3 [−4.8, +7.4] | X− +5.6 [−0.2, +11.4] | +5.5 (34.1) | 0.542 | 0.544 (+3.6) | 0.565 | +2.8, 0.522 | +1.9, 0.514 |
| AU rounds 1–20 [MF2] | X− +14.3 [+6.1, +22.5] | X +9.1 [+0.6, +17.6] | X− +9.2 [+1.0, +17.4] | +10.6 (32.8) | 0.579 | 0.591 (+7.7) | 0.628 | +5.4, 0.546 | +3.2, 0.523 |
| Zhejiang vs AI, rounds 1–20 [MF2] | X+ +6.4 [−2.8, +15.6] | X− +3.6 [−5.7, +12.9] | X+ +0.3 [−8.0, +8.6] | +3.3 (31.8) | 0.524 | 0.529 (+2.5) | 0.541 | +1.7, 0.515 | +0.1, 0.501 |

**Notes on 2a**
- The rounds 1–20 best responses were chosen in-sample from small cells (n = 309–746), so they are optimistic.
- Out-of-sample check, applying each population's full-session best response to its own rounds 1–20 (parametric bootstrap):
  - US "always X−": **+5.0 [+1.6, +8.3]**.
  - AU "always X−": **+8.2 [+3.6, +12.7]**.
  - Zhejiang-vs-AI "always X+": +2.9 [−2.2, +8.0].
- 95% CIs from published SEMs, with a range covering the unknown covariance:
  - Zhejiang a=2, after opp W, X+ +28.1: between [+17.8, +38.3] and [+14.0, +42.2].
  - US after opp L, X− +14.0: between [+10.9, +17.1] and [+9.6, +18.4].
  - US after tie, X− +5.8: between [+2.9, +8.7] and [+1.8, +9.8].
  - AU after opp W, X− +10.3: between [+6.5, +14.1] and [+4.9, +15.7].
  - Dyson 2016 after opp L, X− +14.9: between [+8.4, +21.4] and [+5.9, +23.9].
- Generic lose-shift opponent (after a loss they repeat with probability r and split the rest evenly; uniform otherwise). Throwing X− after their loss gains (1−3r)/2 on that throw:

| Repeat-after-loss r | Gain on post-loss throws | Per-throw edge | Bo3 |
|---|---|---|---|
| 0.177 | +23.5 | +8.5 | 0.559 |
| 0.215 | +17.8 | +6.3 | 0.545 |
| 0.261 | +10.8 | +3.8 | 0.527 |

  (r range 0.177–0.261 from sequential:B3.)

**2b. Robustness across populations: fixed rules against every table** (stationary edge in pp per throw).

| Rule (after opp W / T / L) | ZJ a=2 | ZJ vs AI | Dyson 2016 | Forder & Dyson | Dyson 2021 | US | AU | **Min of 7** | West mean | ZJ mean | US 1–20 | AU 1–20 | ZJ-AI 1–20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 Zhejiang best response X+/X+/X | +17.2 | +8.9 | +0.4 | +3.7 | +1.6 | −1.5 | −6.4 | −6.4 | −0.4 | +13.1 | −2.4 | −6.9 | +2.9 |
| R2 always X+ (beat their last hand) | +13.5 | +12.0 | −6.3 | −2.3 | −3.0 | −6.4 | −10.1 | −10.1 | −5.6 | +12.8 | −4.1 | −9.2 | +2.9 |
| R3 always X− (throw what their last hand beats) | −18.7 | −12.0 | +8.5 | +5.0 | +7.0 | +8.2 | +6.9 | −18.7 | +7.1 | −15.3 | +5.0 | +8.2 | −1.1 |
| **R4 X+/X−/X−** | +3.7 | +2.7 | +10.6 | +13.4 | +10.9 | +7.1 | +0.4 | **+0.4** | **+8.5** | +3.2 | −0.3 | +1.7 | +3.1 |
| R5 X/X−/X− | −5.3 | −6.1 | +10.9 | +9.0 | +7.5 | +5.9 | +4.1 | −6.1 | +7.5 | −5.7 | +0.4 | +1.8 | +0.9 |
| R6 MF1 cycle (throw what your own last hand beats) X+/X−/X | +9.6 | +3.6 | +5.5 | +7.0 | +5.1 | +2.2 | −0.6 | −0.6 | +3.8 | +6.6 | −2.2 | −1.7 | +3.3 |
| R7 C2 rules, random after tie: X+/rand/X | +11.6 | +6.1 | +1.9 | +4.9 | +2.6 | +0.4 | −2.8 | −2.8 | +1.4 | +8.9 | −2.1 | −2.8 | +2.2 |
| R8 task example "beat the previous winning hand": X+/rand/X− | +5.7 | +5.0 | +5.9 | +10.6 | +7.8 | +4.9 | −1.9 | −1.9 | +5.5 | +5.4 | −0.2 | +0.6 | +1.9 |
| R9 rand/X−/X− | −5.7 | −4.6 | +10.0 | +9.4 | +8.6 | +7.1 | +3.9 | −5.7 | +7.8 | −5.2 | +1.8 | +4.1 | +1.0 |
| R10 tie-only X−: rand/X−/rand | −3.0 | −2.9 | +4.2 | +2.7 | +2.8 | +2.0 | +2.0 | −3.0 | +2.7 | −3.0 | −0.1 | +1.0 | +1.2 |
| R11 loss-only X−: rand/rand/X− | −2.6 | −1.8 | +5.2 | +6.3 | +5.3 | +4.9 | +1.8 | −2.6 | +4.7 | −2.2 | +1.9 | +3.2 | −0.2 |

**What the robustness check shows**
- **Brute force over all 64 per-state rules:**
  - R4 is the only rule with a positive minimum across the 7 full tables. It also has the best mean (+6.99).
  - Over all 10 tables R4's worst case is −0.28 (US rounds 1–20; bootstrap [−3.8, +3.3]).
  - The runner-up is X+/X/X− (minimum −0.32, mean +4.46).
- **With opponents' biases halved,** R4 still gives a minimum of +0.1, West mean +4.1 and ZJ mean +1.5.
- **R4 Bo3 win probabilities:** Zhejiang a=2 0.519, ZJ vs AI 0.511, Dyson 2016 0.591, Forder & Dyson 0.610, Dyson 2021 0.591, US 0.560, AU 0.511, US rounds 1–20 0.498, AU rounds 1–20 0.517, ZJ-AI rounds 1–20 0.527.
- **Bootstrap 95% CIs in rounds 1–20:**

| Rule | US | AU | ZJ vs AI |
|---|---|---|---|
| R11 (loss-only X−) | +1.9 [−0.0, +4.0] | +3.2 [+0.3, +6.3] | −0.2 [−2.8, +2.8] |
| R10 (tie-only X−) | −0.1 [−2.1, +1.9] | +1.0 [−1.9, +3.8] | +1.2 [−1.8, +4.2] |
| R2 (always X+) | −4.1 [−7.5, −0.7] | −9.2 [−14.0, −4.5] | +2.9 [−2.2, +8.0] |

---

## 3. After a tie on X

Edges are of X+ (beat the tied hand), X (repeat it) and X− (throw the hand the tied hand beats).

| After-tie data [source] | Opp stay / up / down % | X+ | X | X− | Best response |
|---|---|---|---|---|---|
| Wang & Xu a=1 (tie pays as much as a win) [C08/MF02] | 80.0/13.8/6.0 | +74.1 | −7.8 | −66.3 | X+ |
| Wang a=1.1 [C08] | 60.4/25.3/14.3 | +46.1 | −11.0 | −35.1 | X+ |
| **Wang a=2** [A1] | 43.2/33.4/23.4 | **+19.8** | −10.0 | −9.8 | X+ |
| Wang a=4 / a=9 / a=100 [C08] | 38.8/38.2/23.0; 35.8/34.9/29.1; 36.4/36.8/26.9 | +15.8 / +6.7 / +9.5 | −15.2 / −5.8 / −9.9 | −0.6 / −0.9 / +0.4 | X+ |
| Wang & Xu a=∞ (tie pays 0) [C08/MF02] | 33.8/37.7/28.3 | +5.5 | −9.4 | +3.9 | X+ (both switches positive) |
| Zhejiang vs AI [C2] | 39.4/30.3/30.3 | +9.1 | 0.0 | −9.1 | X+ |
| Dyson 2016, unweighted / hand-weighted [B1/C07] | 27.5/40.1/32.4; 28.7/39.6/31.7 | −4.9 / −3.0 | −7.7 / −7.9 | **+12.6 / +10.9** | X− |
| Forder & Dyson [B2] | 29.3/37.3/33.4 | −4.1 | −3.9 | +8.0 | X− |
| Dyson 2021 Exps 1 / 2 / 3 [MF5] | 29.7/36.6/33.8; 26.3/35.7/38.0; 33.9/35.1/30.9 | −4.1 / −11.7 / +3.0 | −2.8 / +2.3 / −4.2 | +6.9 / +9.4 / +1.2 | X−, X−, X+ |
| US dyads, 11,656 ties [MF01] | 29.1/35.2/35.6 | −6.5 (reported −6.3 [−10.6, −1.7]) | +0.4 | +6.1 (reported **+5.8 [+2.4, +9.1]**) | X− |
| AU pairs, 9,661 ties [MF01] | 28.3/33.7/38.0 | −9.7 (reported −9.8 [−14.0, −5.3]) | +4.3 | +5.4 (reported **+5.4 [+1.2, +9.7]**) | X− |
| US rounds 1–20, n=686 [MF2] | 33.1/32.8/34.1 | −1.0 [−7.1, +5.1] | +1.3 | −0.3 [−6.4, +5.8] | none distinguishable from 0 |
| AU rounds 1–20, n=372 [MF2] | 28.5/31.2/40.3 | −11.8 [−20.1, −3.5] | +9.1 [+0.6, +17.6] | +2.7 [−5.1, +10.5] | X (in-sample) |
| Zhejiang vs AI rounds 1–20, n=310 [MF2] | 32.9/36.5/30.6 | +2.3 [−6.6, +11.2] | −5.9 | +3.6 [−5.7, +12.9] | none distinguishable |
| JP survey, STATED [MF07] | 19.3/36.9/43.8 | −24.5 | +6.9 | +17.6 | X− |
| JP live (assumes after-tie repeat = overall 22.75% and an even split) [C06] | 22.75/38.6/38.6 | −15.9 | 0 | +15.9 | X− (assumption) |

**By tied hand** (edges in pp of throwing X− / X+ / X):

| Data | Rock–Rock: S / P / R | Paper–Paper: R / S / P | Scissors–Scissors: P / R / S |
|---|---|---|---|
| AU [MF01] | +1.0 / −7.8 / +6.8 | +4.4 / −12.3 / +7.9 | +11.8 / −9.6 / −2.2 |
| US [MF01] | +4.0 / −3.9 / −0.1 | +12.4 / −9.3 / −3.1 | +1.7 / −5.9 / +4.2 |
| Dyson 2016 [C07] | +5.1 / +1.4 / −6.5 | +16.0 / −9.5 / −6.5 | +16.8 / −6.6 / −10.2 |

X− is positive in all 9 cells. X+ is negative in 8 of 9.

**Match-level value of a tie-only rule** (R10: X− after ties, random otherwise):
- Per throw: +2.0 to +4.2 pp against Western tables; −3.0 / −2.9 against Zhejiang tables; −0.1 to +1.2 in rounds 1–20.
- Bo3: 0.522–0.547 (West) versus 0.467–0.468 (Zhejiang).

---

## 4. Format amplification

**4a. Match and team win probability as a function of q** (constant q, independent bouts).

| q | 1 decisive throw | Bo3 | Bo5 | Relay n=3 | Relay n=5 | Relay n=7 | 5-member points, 1-throw bouts | 5-member points, Bo3 bouts | 5-member points, Bo5 bouts |
|---|---|---|---|---|---|---|---|---|---|
| 0.50 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 |
| 0.52 | 0.520 | 0.530 | 0.537 | 0.537 | 0.549 | 0.558 | 0.537 | 0.556 | 0.570 |
| 0.55 | 0.550 | 0.575 | 0.593 | 0.593 | 0.621 | 0.644 | 0.593 | 0.638 | 0.671 |
| 0.60 | 0.600 | 0.648 | 0.683 | 0.683 | 0.733 | 0.771 | 0.683 | 0.762 | 0.813 |

- The winner-stays relay equals P(Bin(2n−1, q) ≥ n). This was checked by DP to 1e-12.
- A 3-member points format with Bo3 bouts (team:C3) gives 0.545 / 0.611 / 0.716 for q = 0.52 / 0.55 / 0.60.

**4b. Converting realistic edges to match odds,** using q = ½ + e/(2(1−t)), where t is the tie rate.

| Scenario | e (pp) | t | q | Bo3 | Bo5 | Relay n=5 | Points-5 (Bo3 bouts) |
|---|---|---|---|---|---|---|---|
| Experienced online players, realised [D1/C16] | +1.49 | 32.2% | 0.511 | 0.516 | 0.521 | 0.527 | 0.531 |
| Model best response to predicted play [D1/C16] | +14.29 | 31.0% | 0.604 | 0.653 | 0.689 | 0.741 | 0.770 |
| Persistent Rock bias, always Paper (AU marginals) [MF03] | +3.22 | 32.5% | 0.524 | 0.536 | 0.545 | 0.559 | 0.567 |

- A first-throw-only edge, with all later throws fair, gives **Bo3 = 0.5 + 0.25·e1** and Bo5 = 0.5 + 0.1875·e1:
  - Paper against online openers: e1 = +2.8, Bo3 0.507.
  - Eyler novices: e1 = +43.7, Bo3 0.609.
- Longer formats dilute a first-throw edge and amplify a persistent one.

**4c. Relay add-on: the challenger leans to the hand that beats the champion's last winning hand.** Only our team does this; it applies to the bout's first throw.

| Champion behaviour assumed | Gain on that throw | Relay n=3 / 5 / 7, single-throw bouts | Relay n=3 / 5 / 7, Bo3 bouts |
|---|---|---|---|
| Western new-opponent win-stay 38.2% (B4/team:C15; shifts split evenly) | +7.3 | 0.527 / 0.540 / 0.549 | 0.514 / 0.520 / 0.525 |
| Zhejiang a=2 after-win row (A1; mostly new opponents) | +28.1 | 0.605 / 0.652 / 0.685 | 0.553 / 0.577 / 0.594 |

If champions behave like the AU fixed pairs (win-stay 26.2%), the same lean costs −11.0 pp on that throw.

---

## 5. Team vs host, and simultaneous rounds

**5a. Probability that a simultaneous n-player round is decisive (exactly two hands shown).** Closed form: 3(2^n−2)/3^n = (2^n−2)/3^(n−1), verified by exhaustive enumeration.

| n | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| P(decisive) | 0.667 | 0.667 | 0.519 | 0.370 | 0.255 | 0.173 | 0.116 | 0.078 | 0.052 |
| Expected throws to the first decisive round | 1.50 | 1.50 | 1.93 | 2.70 | 3.92 | 5.79 | 8.61 | 12.86 | 19.26 |

**5b. P(at least one member survives k rounds) against a uniform random host.** Each cell shows independent random play → coordinated even split. The even split equals the exact DP optimum over all splits in all 40 cells. Expected survivors are identical for every strategy: n/3^k under rule A and n(2/3)^k under rule B.

Rule A (only winners survive):

| n | k=1 | k=2 | k=3 | k=4 | k=5 |
|---|---|---|---|---|---|
| 3 | .704 → **1.000** | .298 → .333 | .107 → .111 | .037 → .037 | .012 → .012 |
| 5 | .868 → **1.000** | .445 → .556 | .172 → .185 | .060 → .062 | .020 → .021 |
| 10 | .983 → 1.000 | .692 → **1.000** | .314 → .370 | .117 → .123 | .040 → .041 |
| 20 | 1.000 → 1.000 | .905 → 1.000 | .530 → **.741** | .220 → .247 | .079 → .082 |
| Herding | .333 | .111 | .037 | .012 | .004 |

Rule B (winners and ties survive):

| n | k=1 | k=2 | k=3 | k=4 | k=5 |
|---|---|---|---|---|---|
| 3 | .963 → 1.000 | .829 → **1.000** | .652 → .778 | .483 → .556 | .345 → .383 |
| 5 | .996 → 1.000 | .947 → 1.000 | .827 → **1.000** | .667 → .827 | .506 → .605 |
| 10 | 1.000 | .997 → 1.000 | .970 → 1.000 | .889 → 1.000 | .756 → **.959** |
| 20 | 1.000 | 1.000 | .999 → 1.000 | .988 → 1.000 | .941 → 1.000 |
| Herding | .667 | .444 | .296 | .198 | .132 |

- **Largest gains:** under rule A, n=10/k=2 +30.8 pp, n=3/k=1 +29.6, n=20/k=3 +21.1. Under rule B, n=10/k=5 +20.2, n=5/k=3 +17.3.
- **Biased-host sensitivity** (host follows the JP live marginals 35.0/33.3/31.7): the best-labelled even split stays within 0.8 pp of the full optimum (rule A, n=10, k=3: 0.391 vs 0.399).

**Supplement (not requested): cross-check of team:MF1, simultaneous team vs team.**

| Composition (vs an independent team) | Rule I (more winners wins) | Rule II (only one team has winners) |
|---|---|---|
| 3v3, 2 on X + 1 on X− | 0.6875 (11/16) | 0.6836 (175/256) |
| 3v3, 2 on X + 1 on X+ | 0.3125 | 0.469 |
| 3v3, random orientation | 0.500 | 0.576 |
| 3v3, herding | 0.500 | 0.250 |
| 4v4, 3 on X + 1 on X− | 0.859 | 0.779 |
| 2v2, two different hands | 0.500 | 0.583 |
| 3v3, 2 on X + 1 on X− vs a herding team | 0.500 | 0.875 |

---

## 6. Our exploitability

**6a. Opponent who knows the rule and best-responds every throw.** The per-throw edge is exactly −p after the first throw. Example rule R4 (identical for any rule that is active in every state):

| p (share of throws following the rule) | 0 | 0.1 | 0.2 | 0.3 | 0.5 | 0.75 | 1.0 |
|---|---|---|---|---|---|---|---|
| Edge per throw | 0 | −10 | −20 | −30 | −50 | −75 | −100 |
| P(win), first to 1 | .500 | .476 | .455 | .435 | .400 | .364 | .333 |
| P(win), Bo3 | .500 | .417 | .343 | .277 | .168 | .068 | **.000** |
| P(win), Bo5 | .500 | .385 | .286 | .204 | .089 | .018 | .000 |

The task's example rule (R8) is random after ties. Even so, at p=1 it gives Bo3 0.000, a stationary edge of −100, and first-to-1 of 0.500.

**6b. Gain against non-adapting populations versus loss to an informed opponent.** Gains scale roughly linearly with p.

| Rule | p | West-mean edge (Bo3) | ZJ-mean edge (Bo3) | Worst table | Informed opponent: edge (Bo3) |
|---|---|---|---|---|---|
| R4 X+/X−/X− | 1 / 0.5 / 0.25 | +8.50 (.572) / +4.15 (.536) / +2.05 (.518) | +3.20 (.515) / +1.54 (.506) / +0.75 (.503) | −0.28 / −0.14 / −0.07 | −100 (.000) / −50 (.168) / −25 (.309) |
| R8 example (X+/rand/X−) | 1 / 0.5 / 0.25 | +5.46 (.540) / +2.71 (.520) / +1.35 (.510) | +5.39 (.545) / +2.85 (.523) / +1.47 (.511) | −1.93 / −0.94 / −0.46 | −100 (.000) / −40 (.250) / (.375) |
| R6 MF1 cycle | 1 / 0.5 / 0.25 | +3.83 (.538) / +1.99 (.520) / +1.01 (.510) | +6.59 (.541) / +3.28 (.519) / +1.63 (.509) | −2.18 / −1.08 / −0.54 | −100 / −50 / −25 |
| R1 Zhejiang best response | 1 / 0.5 / 0.25 | −0.44 (.490) / −0.23 (.495) / −0.12 (.497) | +13.05 (.621) / +6.85 (.562) / +3.51 (.531) | −6.94 / −3.40 / −1.69 | −100 / −50 / −25 |

At p=0.4:
- R4: West +3.30 (Bo3 0.529), ZJ +1.22 (0.505); informed opponent Bo3 0.219.
- R8: West +2.17 (0.516), ZJ +2.30 (0.518); informed opponent Bo3 0.300.

**6c. How much humans actually exploit fixed rules.** Data are 90%-deterministic bots over 300 rounds; α = realised / theoretical maximum (0.90).

| Bot rule [sequential:D4, MF1] | Class | Human W/L % | Bot net per round | α |
|---|---|---|---|---|
| prev_move_positive | simple self-transition | 66.5/16.6 | −49.9 | 0.55 |
| opponent_prev_move_nil | simple opponent-transition | 65.0/17.7 | −47.3 | 0.53 |
| prev_move_negative (= MF1 cycle, R6) | simple self-transition | 62.2/17.6 | −44.6 | 0.50 |
| opponent_prev_move_positive | simple opponent-transition | 58.5/12.7 | −45.8 | 0.51 |
| win_nil_lose_positive | outcome-conditioned | 41.3/24.8 | −16.5 | 0.18 |
| win_positive_lose_negative (= "beat the previous winning hand", stays after ties; R8 and R4 are its tie variants) | outcome-conditioned | 39.7/26.7 | −13.0 | **0.14** |
| outcome × transition | dual dependency | 34.1/32.0 | −2.1 | 0.02 |

**6d. Break-even share of opponents who exploit the rule.** Gain and loss are both linear in p, so the share φ* = G/(G+α) does not depend on p.

| Rule's gain G (pp per throw at p=1) | α = 1 (fully informed) | α = 0.50 | α = 0.14 |
|---|---|---|---|
| 8.5 (R4, West mean) | 7.8% | 14.5% | 37.8% |
| 5.0 | 4.8% | 9.1% | 26.3% |
| 2.0 | 2.0% | 3.8% | 12.5% |
| 17.0 | 14.5% | 25.4% | 54.8% |

Rule-specific: R8 with its D4 counterpart's α (0.144) gives φ* ≈ 27%. R6 (G = 3.8, α = 0.50) gives ≈ 7%.

**6e. Detectability.** Expected throws for an ideal observer who already suspects this exact rule to reach 20:1 evidence, ln20 / KL(p):

| p | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.75 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|
| Throws to 20:1 | 308 | 79 | 36 | 20 | 13.0 | 5.6 | 3.7 | 2.7 |

Equivalently, to stay below 20:1 expected evidence: p ≤ 0.90 within one Bo3 (~3.7 throws), ≤ 0.65 within ~7.5 throws, ≤ 0.42 within a fully watched 5-bout relay (~18.5 throws), and ≤ 0.29 within ~37 throws.

**Trade-off summary**
- Each pp of expected gain against a naive population costs 100/G pp per throw against an informed opponent: about 12× for R4 against West-like play and about 31× against Zhejiang-like play.
- Mixing does not change that ratio. What it buys is slower detection (about 3/p² throws) and a non-zero worst case. At p=0.4, R4 gives Bo3 0.529 against West-like opponents and 0.219 against an informed opponent; following it deterministically gives 0.572 and 0.000.

---

## Explicit assumptions

1. All exploitation edges are upper bounds. They assume a non-adapting opponent equal to the population-average table. Heterogeneity (sequential:B5) and adaptation (D3) shrink them. The ×0.5 shrink is equivalent to a 50/50 mixture of table-followers and uniform players, exactly so for per-state edges.
2. Opponents are first-order: the next move depends only on their own last hand and outcome. Table rows not summing to 1 (e.g., A1 W row = 1.001) were renormalised.
3. In match simulations the first throw is uniform for both players and ties are replayed. "Only after-loss bias" means the opponent plays uniformly after its wins and ties.
4. Clustering:
   - First-throw CIs are multinomial Wald.
   - "Adj." CIs use ICC ρ = 0.0166, the larger of the values implied by the reported pair-cluster bootstraps (Moerel 0.0066, Brockbank 0.0166). Wang 2014's player SDs imply about 0.024.
   - m (throws per player) is total throws ÷ players.
   - Rounds 1–20 bootstraps ignore within-player clustering.
5. Derived inputs:
   - Forder & Dyson Paper share = 100 − R − S.
   - Dyson 2022 = mean of 3 conditions, with n = 40×360.
   - Cook n = 14 triads × 9 × 20 × 2.
   - Aczel R = P.
   - Yoshizawa after-tie repeat = overall repeat (22.75%), shifts split evenly.
   - B4 champion shifts split evenly.
   - Dyson 2021 used the Exp 1 no-credit column, the only complete W/T/L table.
6. Formats (Section 4) use a constant q and independent bouts. The relay lean affects only the first throw of each bout.
7. The host is uniform and independent of the team plan. In the sensitivity check the host follows the JP live marginals.
8. The informed opponent knows both the rule and the state. α comes from 300-round sessions against 90% bots, which is longer than tournament bouts. The KL detection horizon assumes the observer already suspects the specific rule, so real detection is slower.
9. The rule selection in 2b is in-sample over 7+3 tables. No Korean data exist, so whether Korean opponents behave like the Zhejiang or the Western tables is the key unknown.

## Methods (one line each)

- **First throw:** exact W/T/L permutations, multinomial-variance Wald CIs, design-effect inflation; small-n rows cross-checked with a percentile bootstrap.
- **Conditional play:** 3-state Markov chain over the opponent's last outcome; stationary edge by linear solve; Bo3/Bo5 by an absorbing chain. Validated by Monte Carlo: Bo3 P(win) within 0.002, long-run edge within 0.2 pp.
- **Robustness:** brute force over all 64 per-state rules; parametric multinomial bootstrap (4,000 draws) for rounds 1–20.
- **Formats:** exact binomial sums; the relay was also solved by DP.
- **Host game:** exact rational DP over survivor allocations; decisive probability by exhaustive enumeration up to 3^10 profiles.
- **Team vs team:** exact rational recursion over all hand profiles.
- **Exploitability:** mixed-policy Markov chain with an informed best-responder; KL-divergence detection horizon.

Files are in /private/tmp/claude-501/-Users-baemanjin-orca-projects-----/9282a235-4fc4-4c50-add0-37a1d5aaa853/scratchpad/model (`all_outputs.log` has every printed result; `data.py` holds every parameter with its source ID).