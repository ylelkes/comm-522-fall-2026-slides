set.seed(522)

n <- 1800
beauty <- runif(n, 0, 10)
talent <- runif(n, 0, 10)
famous <- beauty + talent > 15

r_all <- cor(beauty, talent)
r_famous <- cor(beauty[famous], talent[famous])

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_path <- normalizePath(sub("^--file=", "", script_arg))
out <- file.path(dirname(script_path), "assets", "collider-fame-scatter.png")

png(out, width = 1500, height = 610, res = 150, type = "cairo", bg = "#f7f4ed")
par(
  mfrow = c(1, 2),
  mar = c(4.2, 4.5, 3.4, 1.2),
  oma = c(0, 0, 0, 0),
  family = "sans",
  fg = "#18324a",
  col.axis = "#18324a",
  col.lab = "#18324a"
)

draw_panel <- function(title, subtitle) {
  plot(
    NA,
    xlim = c(0, 10), ylim = c(0, 10),
    xlab = "Conventional screen beauty (simulated)",
    ylab = "Acting talent (simulated)",
    axes = FALSE,
    main = title,
    cex.main = 1.25,
    cex.lab = 0.95
  )
  abline(h = seq(0, 10, 2), v = seq(0, 10, 2), col = "#ded9cf", lwd = 0.8)
  axis(1, at = seq(0, 10, 2), las = 1, cex.axis = 0.85)
  axis(2, at = seq(0, 10, 2), las = 1, cex.axis = 0.85)
  box(col = "#8a969f")
  mtext(subtitle, side = 3, line = 0.35, cex = 0.9, col = "#52616d")
}

draw_panel("All aspiring actors", sprintf("Beauty and talent are independent: r = %.02f", r_all))
points(beauty[!famous], talent[!famous], pch = 16, cex = 0.46, col = adjustcolor("#52616d", alpha.f = 0.22))
points(beauty[famous], talent[famous], pch = 16, cex = 0.62, col = adjustcolor("#b24a3c", alpha.f = 0.78))
abline(a = 15, b = -1, col = "#d39b35", lwd = 2.2, lty = 2)
text(6.05, 9.45, "fame threshold", col = "#9a6c17", cex = 0.82, adj = 0)
legend(
  "bottomleft",
  legend = c("Not selected", "Becomes famous"),
  pch = 16,
  col = c(adjustcolor("#52616d", alpha.f = 0.45), "#b24a3c"),
  bty = "n",
  cex = 0.82
)

draw_panel("Famous actors only", sprintf("Conditioning on fame creates r = %.02f", r_famous))
points(beauty[famous], talent[famous], pch = 16, cex = 0.75, col = adjustcolor("#b24a3c", alpha.f = 0.72))
fit <- lm(talent[famous] ~ beauty[famous])
abline(fit, col = "#18324a", lwd = 3)

dev.off()

cat(sprintf("Created %s with n=%d, famous=%d, r_all=%.03f, r_famous=%.03f\n",
            out, n, sum(famous), r_all, r_famous))
