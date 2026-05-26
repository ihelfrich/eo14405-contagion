# EO 14405 contagion model

Companion code and dossiers for the working paper *Stablecoin Run Risk
Under Direct Federal Reserve Access*. Live versions of the paper, the
long-form blog research note, the 700-word summary, and the OSINT
dossiers are at [ihelfrich.github.io/eo14405-contagion](https://ihelfrich.github.io/eo14405-contagion/).

Tests whether direct Federal Reserve master-account access for stablecoin
issuers (the structural change in [EO 14405](https://www.federalregister.gov/d/2026-10399))
reduces or merely relocates systemic risk relative to the current
bank-deposit-based reserve regime.

## Headline finding

Same shock (an SVB-class regional bank fails), two regimes:

| Metric                                  | Pre-EO   | Post-EO  |
|-----------------------------------------|----------|----------|
| USDC peg trough                         | 0.898    | 0.998    |
| Time to peg restoration                 | 69 h     | 30 h     |
| System-wide contagion score             | 37.05    | 0.43     |
| Peak Fed master-account liquidity draw  | \$0       | \$12.1B   |
| Peak commercial-bank equity drawdown    | \$52B     | \$13B     |

The post-EO regime cuts contagion magnitude by ~99% but transfers the
absorption mechanism onto the Fed's balance sheet. The Fed is now the
counterparty that determines whether a stablecoin run results in a depeg
versus a smooth liquidity backstop.

## Calibration

Pre-EO dynamics calibrated to the USDC March 2023 episode using the
[Fed FEDS Notes post-mortem](https://www.federalreserve.gov/econres/notes/feds-notes/in-the-shadow-of-bank-run-lessons-from-the-silicon-valley-bank-failure-and-its-impact-on-stablecoins-20251217.html):

| Parameter           | Historical (USDC Mar 2023) | Model    |
|---------------------|----------------------------|----------|
| Peg trough          | 0.86                       | 0.898    |
| Trough hour         | ~14h                       | 12h      |
| Recovery hour       | ~72h                       | 69h      |
| Reserve impairment  | 8%                         | 10.2%    |

Errors: |trough| 0.038, |recovery| 3h.

## Data sources

| Item                              | Source                                         | Status     |
|-----------------------------------|-----------------------------------------------|------------|
| USDC reserve composition          | Circle monthly attestation                    | Live page (needs API) |
| USDT reserve composition          | Tether quarterly attestation                  | Live page  |
| Stablecoin market caps            | DefiLlama, CoinGecko                          | Approximate (2026 values) |
| Fed master account list           | Fed.gov; Custodia litigation; press releases  | Partial (Kraken Financial confirmed Mar 2026) |
| Bank size data                    | Q1 2026 call reports, GSIB list               | Approximate |
| USDC/SVB March 2023 hourly prices | Chainalysis, CoinDesk, Fed FEDS Notes         | Documented |
| Treasury yields                   | FRED                                           | Available  |
| MMF AUM (Prime / Government)      | FRED MMMFFAQ027S / OFR MMF data               | Available  |

## What the model does NOT capture

- **Endogenous Fed response function.** The "Fed extends liquidity"
  parameter is binary. A more sophisticated model would derive the
  Fed's reaction function from observable variables (stablecoin
  market cap, redemption velocity, broader credit spreads).
- **Stablecoin-to-MMF substitution.** If USDC depegs, some holders
  migrate to government MMFs. That second-order flow is not modeled.
- **Stablecoin reserve composition heterogeneity.** USDT, DAI, PYUSD
  have meaningfully different reserve mixes that we collapse into a
  single per-issuer share.
- **Operational fiat rails post-EO.** Even with direct Fed access,
  stablecoin issuers need commercial bank relationships for customer
  fiat in/out. That residual exposure (modeled as ~10% at REG_A) is
  approximate.
- **Cross-jurisdiction contagion.** A US bank failure affecting USDT
  (Tether is registered in BVI, custodians elsewhere) has international
  transmission channels we collapse.

## How to run

```bash
pip install matplotlib networkx numpy
python src/model.py --calibrate
python src/model.py --no-fed-liquidity   # worst case: Fed declines support
```

## Methodology

Network model: directed multi-graph with weighted edges representing
USD-denominated obligations. Six node classes: GSIB banks, regional
banks, money market funds, stablecoin issuers, crypto exchanges, the
Federal Reserve.

Dynamics: Eisenberg-Noe (2001) clearing for interbank obligations,
extended with redemption-driven asset fire sales (Cont and Schaanning
2017), code-based amplification via stablecoin Peg Stability Modules
(the channel the Fed identified in its USDC/SVB post-mortem), and a
primary-market suspension paradox where halted redemptions amplify
secondary-market dysfunction.

Shock: an SVB-class regional bank ("REG_B") enters receivership. In
the pre-EO regime, multiple stablecoin issuers have reserves trapped
there. In the post-EO regime, stablecoin reserves are at the Federal
Reserve master account; the bank failure causes panic but does not
directly impair reserves.

Confidence is modeled as a piecewise function over three phases
(panic, plateau, recovery), with the backstop announcement time
regime-dependent (post-EO: 18h reflecting faster Fed reaction with
explicit policy framework; pre-EO: 48h reflecting the historical
USDC/SVB resolution timeline).

## Citation

Helfrich, Ian. 2026. "EO 14405 contagion topology: a network model."
Working note, [github.com/ihelfrich/eo14405-contagion](https://github.com/ihelfrich/eo14405-contagion).
