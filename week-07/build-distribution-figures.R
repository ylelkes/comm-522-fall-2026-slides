set.seed(522)

paper <- "#f7f4ee"
navy <- "#18324a"
blue <- "#2f6687"
rust <- "#b24a3c"
gold <- "#d5aa55"
muted <- "#62717d"

dir.create("assets", showWarnings = FALSE)

draw_density <- function(x, main, subtitle, color, xlim = c(-4, 4)) {
  d <- density(x, from = xlim[1], to = xlim[2], n = 512)
  x_mean <- mean(x)
  x_sd <- sqrt(mean((x - x_mean)^2))
  plot(d, type = "n", xlim = xlim, ylim = c(0, max(d$y) * 1.18),
       axes = FALSE, xlab = "", ylab = "", main = "")
  polygon(d$x, d$y, col = adjustcolor(color, alpha.f = 0.24), border = color, lwd = 4)
  abline(v = x_mean, col = rust, lwd = 3)
  abline(v = x_mean + c(-1, 1) * x_sd, col = navy, lwd = 3, lty = 3)
  axis(1, at = -4:4, labels = -4:4, col.axis = navy, col = muted, cex.axis = 1.2)
  axis(2, labels = FALSE, tick = FALSE, col = muted)
  box(col = "#c8c2b7")
  title(main = main, col.main = navy, font.main = 2, cex.main = 1.65, line = 1)
  mtext(sprintf("%s  •  SD = %.2f", subtitle, x_sd),
        side = 3, line = 0.05, col = muted, cex = 1.0)
  mtext("Political ideology", side = 1, line = 2.7, col = navy, cex = 1.15)
  text(-3.8, max(d$y) * 1.05, "Liberal", adj = 0, col = muted, cex = 1.05)
  text(3.8, max(d$y) * 1.05, "Conservative", adj = 1, col = muted, cex = 1.05)
}

n <- 5000
consensus <- rnorm(n, 0, 0.58)
dispersed <- rnorm(n, 0, 1.55)
polarized <- c(rnorm(n / 2, -1.75, 0.48), rnorm(n / 2, 1.75, 0.48))
consensus <- consensus - mean(consensus)
dispersed <- dispersed - mean(dispersed)
polarized <- polarized - mean(polarized)

png("assets/political-beliefs-same-mean.png", width = 1800, height = 720, res = 150, bg = paper)
par(mfrow = c(1, 3), mar = c(5, 3, 4.5, 1.2), oma = c(0, 0, 0.8, 0), family = "sans")
draw_density(consensus, "Consensus", "Most people near the center", blue)
draw_density(dispersed, "Disagreement", "Views spread across the scale", gold)
draw_density(polarized, "Polarization", "Two opposing clusters", rust)
dev.off()

ideology <- c(-3, -1, -1, 0, 1, 1, 3)
ideology_mean <- mean(ideology)
ideology_sd <- sqrt(mean((ideology - ideology_mean)^2))
nearest_rank <- function(p, x) sort(x)[ceiling(p * length(x))]
q <- vapply(c(.25, .50, .75), nearest_rank, numeric(1), x = ideology)
dots_y <- c(1, 1, 2, 1, 1, 2, 1)

png("assets/ideology-sd-percentiles.png", width = 1800, height = 780, res = 150, bg = paper)
par(mfrow = c(1, 2), mar = c(5, 3, 4.8, 1.4), oma = c(0, 0, 0.7, 0), family = "sans")

plot(NA, xlim = c(-4, 4), ylim = c(0.5, 3.5), axes = FALSE,
     xlab = "", ylab = "", main = "")
rect(-ideology_sd, 0.5, ideology_sd, 3.5, col = adjustcolor(blue, alpha.f = 0.18), border = NA)
abline(h = 1, col = "#c8c2b7", lwd = 2)
abline(v = ideology_mean, col = rust, lwd = 3)
abline(v = c(-ideology_sd, ideology_sd), col = blue, lwd = 3, lty = 2)
points(ideology, dots_y, pch = 21, bg = navy, col = paper, cex = 2.3, lwd = 2)
axis(1, at = -4:4, col.axis = navy, col = muted, cex.axis = 1.15)
axis(2, labels = FALSE, tick = FALSE, col = muted)
box(col = "#c8c2b7")
title(main = "Standard deviation", col.main = navy, font.main = 2, cex.main = 1.65)
mtext("Political ideology", side = 1, line = 2.7, col = navy, cex = 1.15)
text(0, 3.15, "Mean = 0", col = rust, cex = 1.05)
text(-ideology_sd, 2.7, sprintf("−1 SD = %.2f", -ideology_sd), pos = 2, col = blue, cex = 1.0)
text(ideology_sd, 2.7, sprintf("+1 SD = %.2f", ideology_sd), pos = 4, col = blue, cex = 1.0)
text(0, 2.55, "5 of 7 scores inside", col = navy, font = 2, cex = 1.05)

plot(NA, xlim = c(-4, 4), ylim = c(0.5, 3.5), axes = FALSE,
     xlab = "", ylab = "", main = "")
segments(-3, 1, 3, 1, col = gold, lwd = 5)
points(ideology, dots_y, pch = 21, bg = gold, col = paper, cex = 2.3, lwd = 2)
cols <- c(blue, rust, blue)
labs <- c("P25 = −1", "P50 = 0", "P75 = 1")
for (i in seq_along(q)) {
  abline(v = q[i], col = cols[i], lwd = ifelse(i == 2, 4, 3), lty = ifelse(i == 2, 1, 2))
  text(q[i], 3.05 - .35 * (i %% 2), labs[i], col = cols[i],
       font = 2, cex = 1.02, pos = ifelse(i < 2, 2, ifelse(i > 2, 4, 3)))
}
axis(1, at = -4:4, col.axis = navy, col = muted, cex.axis = 1.15)
axis(2, labels = FALSE, tick = FALSE, col = muted)
box(col = "#c8c2b7")
title(main = "Percentiles", col.main = navy, font.main = 2, cex.main = 1.65)
mtext("Political ideology", side = 1, line = 2.7, col = navy, cex = 1.15)
text(-3.7, 3.25, "Nearest-rank convention", adj = 0, col = muted, cex = 1.0)

mtext("The same seven ideology scores used in the calculations", outer = TRUE,
      side = 3, line = -0.15, col = navy, font = 2, cex = 1.4)
dev.off()

# Empirical rule for an approximately normal distribution.
x_norm <- seq(-3.6, 3.6, length.out = 1200)
y_norm <- dnorm(x_norm)
band_col <- function(z) {
  ifelse(abs(z) <= 1, adjustcolor(blue, alpha.f = .55),
         ifelse(abs(z) <= 2, adjustcolor(gold, alpha.f = .55),
                ifelse(abs(z) <= 3, adjustcolor(rust, alpha.f = .42), adjustcolor(muted, alpha.f = .12))))
}

png("assets/normal-sd-empirical-rule.png", width = 1800, height = 820, res = 150, bg = paper)
par(mar = c(6.4, 3.2, 2.2, 1.3), family = "sans")
plot(x_norm, y_norm, type = "n", axes = FALSE, xlab = "", ylab = "",
     xlim = c(-3.65, 3.65), ylim = c(-.125, .43))
for (i in seq_len(length(x_norm) - 1)) {
  polygon(c(x_norm[i], x_norm[i], x_norm[i + 1], x_norm[i + 1]),
          c(0, y_norm[i], y_norm[i + 1], 0),
          col = band_col((x_norm[i] + x_norm[i + 1]) / 2), border = NA)
}
lines(x_norm, y_norm, col = navy, lwd = 4)
abline(v = -3:3, col = adjustcolor(navy, alpha.f = .38), lty = 3, lwd = 2)
axis(1, at = -3:3,
     labels = c(expression(mu-3*sigma), expression(mu-2*sigma), expression(mu-sigma),
                expression(mu), expression(mu+sigma), expression(mu+2*sigma), expression(mu+3*sigma)),
     col.axis = navy, col = muted, cex.axis = 1.15, padj = .5)
axis(2, labels = FALSE, tick = FALSE, col = muted)
box(col = "#c8c2b7")

segments(-1, -.025, 1, -.025, col = blue, lwd = 5)
text(0, -.041, "About 68% within 1 SD", col = blue, font = 2, cex = 1.22)
segments(-2, -.061, 2, -.061, col = gold, lwd = 5)
text(0, -.077, "About 95% within 2 SDs", col = "#8A6A25", font = 2, cex = 1.22)
segments(-3, -.097, 3, -.097, col = rust, lwd = 5)
text(0, -.113, "About 99.7% within 3 SDs", col = rust, font = 2, cex = 1.22)
dev.off()

base_income <- rlnorm(n, meanlog = log(60000), sdlog = 0.32)
top_heavy <- c(rlnorm(round(n * 0.94), meanlog = log(56000), sdlog = 0.38),
               rlnorm(round(n * 0.06), meanlog = log(420000), sdlog = 0.55))
base_income <- base_income * 60000 / median(base_income)
top_heavy <- top_heavy * 60000 / median(top_heavy)

draw_income <- function(x, main, color) {
  cap <- 600000
  breaks <- seq(0, cap, by = 15000)
  h <- hist(pmin(x, cap), breaks = breaks, plot = FALSE)
  plot(h, freq = FALSE, col = adjustcolor(color, alpha.f = 0.28), border = paper,
       axes = FALSE, xlab = "", ylab = "", main = "", xlim = c(0, cap))
  axis(1, at = seq(0, cap, by = 100000),
       labels = paste0("$", seq(0, 600, by = 100), "k"), col.axis = navy,
       col = muted, cex.axis = 1.05)
  axis(2, labels = FALSE, tick = FALSE, col = muted)
  box(col = "#c8c2b7")
  abline(v = median(x), col = navy, lwd = 3, lty = 2)
  abline(v = mean(x), col = rust, lwd = 3)
  title(main = main, col.main = navy, font.main = 2, cex.main = 1.6, line = 1)
  mtext("Annual household income", side = 1, line = 2.8, col = navy, cex = 1.15)
  legend("topright",
         legend = c(sprintf("Median: $%dk", round(median(x) / 1000)),
                    sprintf("Mean: $%dk", round(mean(x) / 1000))),
         col = c(navy, rust), lty = c(2, 1), lwd = 3, bty = "n", cex = 1.05,
         text.col = navy)
}

png("assets/income-same-median.png", width = 1800, height = 760, res = 150, bg = paper)
par(mfrow = c(1, 2), mar = c(5, 3, 4.5, 1.2), oma = c(0, 0, 1, 0), family = "sans")
draw_income(base_income, "Moderate upper tail", blue)
draw_income(top_heavy, "Small group with very high incomes", rust)
mtext("Both populations have median income = $60,000", outer = TRUE, side = 3,
      line = -0.15, col = navy, font = 2, cex = 1.4)
dev.off()
