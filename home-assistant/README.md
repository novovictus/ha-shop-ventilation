# Home Assistant Automations

This directory contains the last working field baseline for the shop nighttime heat-extraction system.

The two automations are currently disabled in the deployed Home Assistant instance while the system is under review:

- [`automations/shop-night-heat-extraction-start.yaml`](automations/shop-night-heat-extraction-start.yaml)
- [`automations/shop-night-heat-extraction-stop.yaml`](automations/shop-night-heat-extraction-stop.yaml)

These are separate Home Assistant UI automation exports. They preserve the known-good July 2026 paired damper/blower baseline and should be imported as two separate automations.

Proposed control changes should be documented and tested separately before replacing this baseline.
