paper <- "#f7f4ee"
navy <- "#18324a"
blue <- "#2f6687"
rust <- "#b24a3c"
muted <- "#62717d"
line <- "#c8c2b7"

load(path.expand("~/Desktop/dime_recipients_1979_2024.rdata"))

senators <- subset(
  cands,
  election == "fd2024" & seat == "federal:senate" & ico.status == "I",
  select = c(name, party, state, composite.score)
)
senators <- senators[!is.na(senators$composite.score), ]
senators <- senators[order(senators$composite.score), ]

liberal <- head(senators, 10)
conservative <- tail(senators, 10)

pretty_names <- c(
  "warren, elizabeth" = "Elizabeth Warren",
  "baldwin, tammy" = "Tammy Baldwin",
  "booker, cory a" = "Cory Booker",
  "sanders, bernard" = "Bernie Sanders",
  "hirono, mazie k" = "Mazie Hirono",
  "merkley, jeffrey alan" = "Jeff Merkley",
  "smith, tina" = "Tina Smith",
  "markey, edward sen" = "Ed Markey",
  "ossoff, t jonathan" = "Jon Ossoff",
  "cortez masto, catherine" = "Catherine Cortez Masto",
  "scott, rick sen" = "Rick Scott",
  "budd, theodore p" = "Ted Budd",
  "schmitt, eric" = "Eric Schmitt",
  "hawley, joshua david sen" = "Josh Hawley",
  "cruz, rafael edward ted" = "Ted Cruz",
  "braun, mike" = "Mike Braun",
  "paul, rand" = "Rand Paul",
  "lee, mike" = "Mike Lee",
  "vance, j d" = "J. D. Vance",
  "tuberville, thomas h" = "Tommy Tuberville"
)

liberal$label <- unname(pretty_names[liberal$name])
conservative$label <- unname(pretty_names[conservative$name])

write.csv(
  rbind(transform(liberal, group = "Most liberal"),
        transform(conservative, group = "Most conservative")),
  "assets/cf-senators-2024-extremes.csv",
  row.names = FALSE
)

draw_rank <- function(dat, side, color, title) {
  dat <- dat[order(dat$composite.score), ]
  y <- seq_len(nrow(dat))
  if (side == "left") {
    xlim <- c(-7.2, 0)
    label_x <- -7.05
    text_adj <- 0
  } else {
    xlim <- c(0, 7.2)
    label_x <- 7.05
    text_adj <- 1
  }
  plot(NA, xlim = xlim, ylim = c(0.4, nrow(dat) + 0.6), axes = FALSE,
       xlab = "", ylab = "", main = "")
  abline(v = 0, col = line, lwd = 2)
  segments(0, y, dat$composite.score, y, col = adjustcolor(color, .45), lwd = 4)
  points(dat$composite.score, y, pch = 21, bg = color, col = paper, lwd = 2, cex = 1.75)
  text(label_x, y, dat$label, adj = text_adj, col = navy, cex = .97, font = 2)
  score_adj <- if (side == "left") 1 else 0
  score_pos <- dat$composite.score + if (side == "left") -.12 else .12
  text(score_pos, y, sprintf("%.2f", dat$composite.score), adj = score_adj,
       col = muted, cex = .88)
  ticks <- if (side == "left") seq(-5, 0, 1) else seq(0, 5, 1)
  axis(1, at = ticks, col.axis = navy, col = muted, cex.axis = 1.0)
  box(col = line)
  title(main = title, col.main = color, font.main = 2, cex.main = 1.55)
  mtext("DIME composite score", side = 1, line = 2.6, col = navy, cex = 1.05)
}

png("assets/cf-senators-2024-extremes.png", width = 1800, height = 920,
    res = 150, bg = paper)
par(mfrow = c(1, 2), mar = c(5, 1.5, 6, 1.5), oma = c(0, 0, 0, 0), family = "sans")
draw_rank(liberal, "left", blue, "Ten lowest scores")
draw_rank(conservative, "right", rust, "Ten highest scores")
dev.off()
