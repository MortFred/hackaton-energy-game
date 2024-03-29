Tasks

- change sliders to capacity input: " xxx GW installed" and as output "~ # of plants"
    (List of MW per Plant will be provided. As first values: 2GW per nuclear plant, 5.4MW per wind turbine onshore, 8.6MW per wind turbine offshore)

- Simulating per time step: Add all possible energy capacities up (100% of the fossil capacities and x% of the renewables according to the time series) and then cut down to minimum load according to the priority. Starting from the cutting down: 1 Oil, 2 Coal, 3 Gas, 4 Wind, 5 Hydro, 6 Solar, Nuclear is uncuttable)

- Weeks chosen: 4 representative weeks? Calculate the score first of all for these 4 weeks and eventually extend the internal calculation later on to a year (but still just show 4 weeks).

Scaling:
- For costs: overall_cost = CAPEX_per_MW * Capacity_installed + OPEX_per_MWh * MWh_produced (<- adding all sources)
              Cost-file for sources will be provided
- Cost scaling: Interpolate the score with cost_per_MWh = overall_cost / overall_MWh_produced for 300€ per MWh is a 0% and 50€ per MWh is a 100% score.

- For CO2-Emissions: total_emissions = C02_emissions_per_MWh * MWh_produced for each power plant, added for each time step. 
   the CO2-score is in a list that scores Co2_per_MWh_produced = total_emissions/overall MWh_produced

- Stability: Per time step 100% security is if the possible_production_MW is >=15% of the overall_maximum_demand_MW on top of the current_demand_MW. 0% is if possible_production_MW is <= current_demand_MW. For the score, all percentages are multiplied together, so that always having +15% possible capacity is 100% overall security and having an underproduction at one point (alias Black-out) is 0%.

- Recheck carbon taxes

- Multiply all three scores together for the final score (whether each score is from 0 to 1 are from 1 to 10 could still be decided)
IDEAS:
- storage: Similar to a generator (will have a MW Capacity and a CAPEX and OPEX) capacity started with 50% loaded (becomes less important when the simulation will be run for a year)
- interconnections: implemented as in and export price.
- switch for "smart grid" to improve the stability scole. Maybe put in the % of flexibility that a consumer demand is flexible (smart electric vehicle loading, industrial operation etc.). It will within this % then in- or decrease the MWh_demand according to the possible_MWh_production.
