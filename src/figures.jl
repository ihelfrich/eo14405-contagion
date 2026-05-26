#=
figures.jl — Helfrich-palette publication figures via CairoMakie.

Consumes the JSON output of the Python analysis pipeline (analyze.py
writes `figures/analysis_data.json` which contains every numerical
result), renders the nine-panel figure with publication typography,
vector PDF + high-DPI PNG output. Cairo backend for crisp text and
vector-faithful export, no rasterized hacks.

Run with:
    julia --project=. src/figures.jl

Reads:  figures/analysis_data.json
Writes: figures/analysis_helfrich.pdf
        figures/analysis_helfrich.png
        figures/individual/<panel>.pdf (one per panel)
=#

using CairoMakie
using Colors
using JSON
using LaTeXStrings
using Statistics
using LinearAlgebra

# ---------------------------------------------------------------------
# Heritage palette (identical hex to Python src/style.py)
# Drawn from UNC Chapel Hill, Georgia Tech, BGSE, Indiana University.
# Documented in docs/style-guide.md.
# ---------------------------------------------------------------------
const CAROLINA_BLUE   = colorant"#4B9CD3"
const CAROLINA_NAVY   = colorant"#13294B"
const OLD_GOLD        = colorant"#B3A369"
const BSE_TEAL        = colorant"#2C7873"
const INDIANA_CRIMSON = colorant"#990000"
const PARCHMENT       = colorant"#FAF8F3"
const SLATE           = colorant"#4E5667"
const MIST            = colorant"#E8E2D5"

# Backward-compatible aliases (so existing panel code continues to work)
const INK    = CAROLINA_NAVY
const RUST   = INDIANA_CRIMSON
const SAGE   = BSE_TEAL
const GOLD   = OLD_GOLD
const VIOLET = colorant"#6a5acd"
const DIM    = SLATE
const TEAL   = BSE_TEAL
const EDGE   = colorant"#444444"

const SEQ_BLUES = [colorant"#E3EEF7", colorant"#B8D3E8", colorant"#7FB1D3",
                   CAROLINA_BLUE, CAROLINA_NAVY]
const SEQ_GOLDS = [colorant"#F4EFDC", colorant"#E0D2A4", colorant"#C7B97A",
                   OLD_GOLD, colorant"#7E6F3B"]
const DIV_BLUE_GOLD = [CAROLINA_NAVY, CAROLINA_BLUE, colorant"#B8D3E8",
                       PARCHMENT, colorant"#E0D2A4", OLD_GOLD,
                       colorant"#7E6F3B"]
# Legacy aliases
const SEQ_WARM      = SEQ_GOLDS
const DIV_BLUE_RUST = DIV_BLUE_GOLD

# ---------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------
function helfrich_theme()
    Theme(
        fontsize        = 11,
        font            = "DejaVu Sans",
        backgroundcolor = :white,
        Axis = (
            xgridcolor   = (DIM, 0.22),
            ygridcolor   = (DIM, 0.22),
            xgridwidth   = 0.6,
            ygridwidth   = 0.6,
            topspinevisible   = false,
            rightspinevisible = false,
            bottomspinecolor  = EDGE,
            leftspinecolor    = EDGE,
            spinewidth        = 0.9,
            xtickcolor   = EDGE,
            ytickcolor   = EDGE,
            xticksize    = 4, yticksize = 4,
            xtickwidth   = 0.8, ytickwidth = 0.8,
            xticklabelsize = 10, yticklabelsize = 10,
            xlabelsize   = 11, ylabelsize = 11,
            titlesize    = 12.5,
            titlealign   = :left,
            titlecolor   = INK,
            titlefont    = "DejaVu Sans Bold",
            titlegap     = 8,
        ),
        Legend = (
            framevisible = false,
            patchsize    = (14, 8),
            rowgap       = 2,
            labelsize    = 10,
        ),
    )
end

set_theme!(helfrich_theme())

# ---------------------------------------------------------------------
# Panel renderers — each takes an Axis and the relevant subset of data
# ---------------------------------------------------------------------

function panel_calibration!(ax, data)
    sim_pre  = data["sim_pre"]
    sim_post = data["sim_post"]
    empir_h  = data["usdc_empirical_hours"]
    empir_p  = data["usdc_empirical_peg"]
    lines!(ax, Float64.(sim_pre["hours"]),  Float64.(sim_pre["usdc_peg"]),
           color = INK,  linewidth = 2.0, label = "Pre-EO")
    lines!(ax, Float64.(sim_post["hours"]), Float64.(sim_post["usdc_peg"]),
           color = RUST, linewidth = 2.0, label = "Post-EO")
    hlines!(ax, 1.0, color = DIM, linewidth = 0.7, linestyle = :dash)
    scatter!(ax, Float64.(empir_h), Float64.(empir_p),
             color = :black, markersize = 6, label = "USDC Mar 2023")
    ax.title = "(a) USDC peg path"
    ax.xlabel = "hours since shock"
    ax.ylabel = "USDC peg (USD)"
    ax.limits = ((0, 96), (0.83, 1.02))
    axislegend(ax, position = :rb, framevisible = false)
end

function panel_bayes!(ax, data)
    band = data["bayes_band"]
    hrs = 0:(length(band["median"]) - 1)
    band!(ax, Float64.(collect(hrs)),
          Float64.(band["lower"]), Float64.(band["upper"]),
          color = (RUST, 0.20))
    lines!(ax, Float64.(collect(hrs)), Float64.(band["median"]),
           color = RUST, linewidth = 2.0, label = "post-EO posterior median")
    sim_pre  = data["sim_pre"]
    lines!(ax, Float64.(sim_pre["hours"][1:73]), Float64.(sim_pre["usdc_peg"][1:73]),
           color = INK, linewidth = 1.6, linestyle = :dash,
           label = "pre-EO (calibrated)")
    hlines!(ax, 1.0, color = DIM, linewidth = 0.7, linestyle = :dash)
    ax.title  = "(b) Bayesian counterfactual"
    ax.xlabel = "hours since shock"
    ax.ylabel = "USDC peg (USD)"
    ax.limits = ((0, 72), (0.83, 1.02))
    axislegend(ax, position = :rb, framevisible = false)
end

function panel_ot!(ax, data)
    sevs_pre  = Float64.(data["ot_sev_pre_x"])
    W_pre     = Float64.(data["ot_sev_pre_y"])
    sevs_post = Float64.(data["ot_sev_post_x"])
    W_post    = Float64.(data["ot_sev_post_y"])
    lines!(ax, sevs_pre  .* 100, W_pre,  color = INK,  linewidth = 2.0, label = "Pre-EO")
    lines!(ax, sevs_post .* 100, W_post, color = RUST, linewidth = 2.0, label = "Post-EO")
    ax.title  = "(c) Wasserstein run severity"
    ax.xlabel = "shock severity (% of USDC reserves)"
    ax.ylabel = L"W_1(\mu_0,\mu_1)\ \text{(bp} \cdot \text{mass)}"
    axislegend(ax, position = :lt, framevisible = false)
end

function panel_globalgame!(ax, data)
    rs = Float64.(data["gg_r_grid"])
    theta_pre  = Float64.(data["gg_theta_pre"])
    theta_post = Float64.(data["gg_theta_post"])
    lines!(ax, rs .* 100, theta_pre,  color = INK,  linewidth = 2.0, label = "Pre-EO")
    lines!(ax, rs .* 100, theta_post, color = RUST, linewidth = 2.0, label = "Post-EO")
    scatter!(ax, Float64[0.5, 4.5],
             [data["gg_theta_star_pre"], data["gg_theta_star_post"]],
             color = :black, markersize = 8)
    ax.title  = "(d) Global-game run threshold"
    ax.xlabel = "rollover yield r (%)"
    ax.ylabel = L"\theta^\star"
    axislegend(ax, position = :rt, framevisible = false)
end

function panel_spectral!(ax, data)
    labels   = ["λ_max", "λ₂", "spectral gap", "Fiedler"]
    pre_vals  = Float64.(data["spectral_pre"])
    post_vals = Float64.(data["spectral_post"])
    n = length(labels); x = 1:n; w = 0.36
    barplot!(ax, x .- w/2, pre_vals,  width = w, color = INK,  label = "Pre-EO")
    barplot!(ax, x .+ w/2, post_vals, width = w, color = RUST, label = "Post-EO")
    hlines!(ax, 1.0, color = DIM, linewidth = 0.7, linestyle = :dash)
    text!(ax, 0.5, 1.03, text = "AOT-S amplification threshold (λ_max = 1)",
          color = DIM, fontsize = 9, align = (:left, :bottom))
    ax.xticks = (1:n, labels)
    ax.ylabel = "eigenvalue magnitude"
    ax.title  = "(e) Spectral contagion metrics"
    axislegend(ax, position = :rt, framevisible = false)
end

function panel_katz!(ax, data)
    labels = data["katz_labels"]
    pre_vals  = Float64.(data["katz_pre"])
    post_vals = Float64.(data["katz_post"])
    n = length(labels); y = 1:n; w = 0.36
    barplot!(ax, y .- w/2, pre_vals, width = w, direction = :x,
             color = INK,  label = "Pre-EO")
    barplot!(ax, y .+ w/2, post_vals, width = w, direction = :x,
             color = RUST, label = "Post-EO")
    ax.yticks = (1:n, labels)
    ax.xlabel = L"\text{Katz centrality } \kappa_i"
    ax.title  = "(f) Super-spreader ranking"
    axislegend(ax, position = :rb, framevisible = false)
end

function panel_welfare!(ax, data)
    classes = ["Holders", "Banks", "Taxpayers"]
    pre  = Float64.(data["welfare_pre"])
    post = Float64.(data["welfare_post"])
    n = length(classes); x = 1:n; w = 0.36
    barplot!(ax, x .- w/2, pre,  width = w, color = INK,  label = "Pre-EO")
    barplot!(ax, x .+ w/2, post, width = w, color = RUST, label = "Post-EO")
    ax.xticks = (1:n, classes)
    ax.ylabel = "loss (USD bn)"
    ax.title  = "(g) Welfare incidence by agent class"
    axislegend(ax, position = :rt, framevisible = false)
end

function panel_en!(ax, data)
    metrics = ["GY amplification", "cascade depth", "defaults"]
    pre  = Float64.(data["en_pre"])
    post = Float64.(data["en_post"])
    n = length(metrics); x = 1:n; w = 0.36
    barplot!(ax, x .- w/2, pre,  width = w, color = INK,  label = "Pre-EO")
    barplot!(ax, x .+ w/2, post, width = w, color = RUST, label = "Post-EO")
    ax.xticks = (1:n, metrics)
    ax.title  = "(h) Eisenberg-Noe cascade structure"
    axislegend(ax, position = :rt, framevisible = false)
end

function panel_indiff!(ax, data)
    d = Float64.(data["welfare_delta"])  # [Delta_H, Delta_B, Delta_T]
    omH = collect(0.0:0.01:1.0)
    omT = collect(0.0:0.01:1.0)
    Z = [(-((1 - oh - ot) * d[2] + oh * d[1] + ot * d[3]))
         for oh in omH, ot in omT]
    # Mask omega_B < 0 region (above the omH + omT = 1 line)
    mask = [oh + ot > 1 for oh in omH, ot in omT]
    Zmasked = [m ? NaN : z for (z, m) in zip(Z, mask)]
    cf = contourf!(ax, omH, omT, Zmasked, levels = 15,
                   colormap = cgrad(DIV_BLUE_RUST))
    contour!(ax, omH, omT, Zmasked, levels = [0.0], color = :black,
             linewidth = 1.4, linestyle = :dash)
    scatter!(ax, [1/3], [1/3], color = :black, marker = :star5, markersize = 12)
    text!(ax, 1/3 + 0.02, 1/3 + 0.03, text = "equal weights", fontsize = 9)
    ax.xlabel = L"\text{holder weight } \omega_H"
    ax.ylabel = L"\text{taxpayer weight } \omega_T"
    ax.title  = "(i) Welfare gain surface"
    Colorbar(ax.parent[ax.layoutobservables.gridcontent[].span.rows.stop,
                       ax.layoutobservables.gridcontent[].span.cols.stop + 1],
             cf, label = "welfare gain (USD bn)", width = 14)
end

# ---------------------------------------------------------------------
# Master layout
# ---------------------------------------------------------------------

function build_figure(data)
    fig = Figure(size = (1500, 1100))
    Label(fig[0, 1:3],
          "EO 14405 contagion analysis: nine-layer evaluation under the Acemoglu-Ozdaglar-Tahbaz-Salehi (2015) framework",
          fontsize = 14, color = INK, halign = :center, font = "DejaVu Sans Bold")
    # 3 x 3 grid
    ax_a = Axis(fig[1, 1]); panel_calibration!(ax_a, data)
    ax_b = Axis(fig[1, 2]); panel_bayes!(ax_b, data)
    ax_c = Axis(fig[1, 3]); panel_ot!(ax_c, data)
    ax_d = Axis(fig[2, 1]); panel_globalgame!(ax_d, data)
    ax_e = Axis(fig[2, 2]); panel_spectral!(ax_e, data)
    ax_f = Axis(fig[2, 3]); panel_katz!(ax_f, data)
    ax_g = Axis(fig[3, 1]); panel_welfare!(ax_g, data)
    ax_h = Axis(fig[3, 2]); panel_en!(ax_h, data)
    ax_i = Axis(fig[3, 3]); panel_indiff!(ax_i, data)
    Label(fig[4, 1:3],
          "Calibration: USDC Mar 2023 episode (Fed FEDS Notes 17 Dec 2025). " *
          "Methods: Eisenberg-Noe clearing, Morris-Shin global game, optimal transport, AOT-S spectral, " *
          "Page-Gong endogenous DSG, Metropolis-Hastings MCMC, Negishi welfare. " *
          "Source: github.com/ihelfrich/eo14405-contagion",
          fontsize = 9, color = DIM, halign = :center)
    return fig
end


function main()
    here = dirname(dirname(abspath(@__FILE__)))
    data_path = joinpath(here, "figures", "analysis_data.json")
    if !isfile(data_path)
        error("Expected $data_path. Run `python src/analyze.py --emit-json` first.")
    end
    data = JSON.parsefile(data_path)
    fig = build_figure(data)
    out_pdf = joinpath(here, "figures", "analysis_helfrich.pdf")
    out_png = joinpath(here, "figures", "analysis_helfrich.png")
    save(out_pdf, fig)
    save(out_png, fig, px_per_unit = 2.5)
    println("Saved: $out_pdf")
    println("Saved: $out_png")
end

main()
