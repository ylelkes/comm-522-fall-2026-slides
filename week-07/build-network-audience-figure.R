library(tidyverse)

users <- tibble(
  id = paste0("U", 1:18),
  cluster = rep(c("Progressive-following users", "Conservative-following users", "Cross-cutting users"), c(7, 7, 4)),
  x = c(-2.8, -2.5, -2.2, -2.7, -2.1, -2.45, -1.9,
         2.8, 2.5, 2.2, 2.7, 2.1, 2.45, 1.9,
         -0.45, -0.15, 0.2, 0.5),
  y = c(1.8, 1.25, 0.75, 0.2, -0.35, -0.9, -1.45,
        1.8, 1.25, 0.75, 0.2, -0.35, -0.9, -1.45,
        1.05, 0.35, -0.35, -1.05)
)

accounts <- tribble(
  ~id, ~label, ~kind, ~x, ~y,
  "LP1", "Progressive\nelite 1", "Political account", -4.45, 1.15,
  "LP2", "Progressive\nelite 2", "Political account", -4.45, -0.15,
  "RP1", "Conservative\nelite 1", "Political account", 4.45, 1.15,
  "RP2", "Conservative\nelite 2", "Political account", 4.45, -0.15,
  "MA", "Outlet A", "Media outlet", -1.25, -2.5,
  "MB", "Outlet B", "Media outlet", 0, -2.5,
  "MC", "Outlet C", "Media outlet", 1.25, -2.5
)

edge_list <- bind_rows(
  expand_grid(from = paste0("U", 1:7), to = c("LP1", "LP2")) %>%
    filter(!(from %in% c("U2", "U5") & to == "LP2")),
  expand_grid(from = paste0("U", 8:14), to = c("RP1", "RP2")) %>%
    filter(!(from %in% c("U9", "U13") & to == "RP2")),
  tibble(from = paste0("U", 15:18), to = c("LP1", "RP1", "LP2", "RP2")),
  tibble(from = paste0("U", 1:7), to = c("MA", "MA", "MA", "MA", "MB", "MA", "MB")),
  tibble(from = paste0("U", 8:14), to = c("MC", "MC", "MC", "MC", "MB", "MC", "MB")),
  tibble(from = paste0("U", 15:18), to = c("MB", "MB", "MB", "MB"))
)

nodes <- bind_rows(
  users %>% transmute(id, label = id, kind = "User", x, y, cluster),
  accounts %>% mutate(cluster = kind)
)

edges <- edge_list %>%
  left_join(nodes %>% select(from = id, x_from = x, y_from = y), by = "from") %>%
  left_join(nodes %>% select(to = id, x_to = x, y_to = y), by = "to")

cluster_colors <- c(
  "Progressive-following users" = "#4C78A8",
  "Conservative-following users" = "#E45756",
  "Cross-cutting users" = "#8A8A8A"
)

p <- ggplot() +
  annotate("rect", xmin = -3.25, xmax = -1.55, ymin = -1.8, ymax = 2.1,
           fill = "#4C78A8", alpha = .07) +
  annotate("rect", xmin = 1.55, xmax = 3.25, ymin = -1.8, ymax = 2.1,
           fill = "#E45756", alpha = .07) +
  geom_segment(
    data = edges,
    aes(x = x_from, y = y_from, xend = x_to, yend = y_to),
    color = "#A8AFB8", linewidth = .45, alpha = .48
  ) +
  geom_point(
    data = users,
    aes(x, y, fill = cluster), shape = 21, color = "white", stroke = .7, size = 4.6
  ) +
  geom_point(
    data = accounts %>% filter(kind == "Political account"),
    aes(x, y), shape = 24, fill = "#F2C14E", color = "#514A32", size = 6
  ) +
  geom_point(
    data = accounts %>% filter(kind == "Media outlet"),
    aes(x, y), shape = 22, fill = "#55A868", color = "#24452A", size = 7
  ) +
  geom_text(
    data = accounts %>% filter(kind == "Political account"),
    aes(x, y, label = label), size = 3.7, lineheight = .9,
    nudge_y = -.72, color = "#2D333A"
  ) +
  geom_text(
    data = accounts %>% filter(kind == "Media outlet"),
    aes(x, y, label = label), size = 4.2, fontface = "bold",
    nudge_y = .58, color = "#2D333A"
  ) +
  annotate("text", x = -2.4, y = 2.38, label = "Users clustered by political follows",
           color = "#4C78A8", fontface = "bold", size = 4.4) +
  annotate("text", x = 2.4, y = 2.38, label = "Users clustered by political follows",
           color = "#E45756", fontface = "bold", size = 4.4) +
  annotate("text", x = 0, y = -3.22,
           label = "Aggregate the inferred ideology of each outlet's followers → audience-alignment score",
           color = "#2D333A", fontface = "bold", size = 4.3) +
  scale_fill_manual(values = cluster_colors) +
  coord_equal(xlim = c(-5.2, 5.2), ylim = c(-3.55, 2.75), clip = "off") +
  labs(
    title = "A network approach: infer users first, then characterize media audiences",
    subtitle = "Circles are users • triangles are political accounts • squares are media outlets",
    fill = NULL
  ) +
  theme_void(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 20, color = "#18212B", margin = margin(b = 5)),
    plot.subtitle = element_text(size = 13, color = "#5B6570", margin = margin(b = 10)),
    legend.position = "none",
    plot.margin = margin(15, 25, 20, 25),
    plot.background = element_rect(fill = "#FAFBFC", color = NA)
  )

ggsave(
  "assets/network-audience-alignment.png", p,
  width = 13.5, height = 7.6, units = "in", dpi = 180, bg = "#FAFBFC"
)

# Two-stage version for distinguishing network description from interpretation.
set.seed(522)
community_nodes <- tibble(
  id = paste0("P", 1:22),
  community = rep(c("Community 1", "Community 2"), each = 11),
  ideology = rep(c("Mostly progressive political follows", "Mostly conservative political follows"), each = 11),
  angle = rep(seq(0, 2 * pi, length.out = 12)[-12], 2),
  radius = rep(c(1.05, .78, 1.18, .88, 1.02, .72, 1.12, .82, 1.2, .92, .68), 2),
  x = if_else(community == "Community 1", -1.9, 1.9) + radius * cos(angle),
  y = radius * sin(angle)
)

within_edges <- map_dfr(c("Community 1", "Community 2"), function(g) {
  ids <- community_nodes %>% filter(community == g) %>% pull(id)
  tibble(
    from = c(ids, ids[c(1, 2, 4, 5, 7, 8, 10)]),
    to = c(dplyr::lead(ids, default = ids[1]), ids[c(4, 6, 7, 9, 10, 1, 3)])
  )
})

between_edges <- tribble(
  ~from, ~to,
  "P3", "P15",
  "P6", "P19",
  "P9", "P13"
)

community_edges <- bind_rows(within_edges, between_edges) %>%
  mutate(
    between = (as.integer(str_remove(from, "P")) <= 11) != (as.integer(str_remove(to, "P")) <= 11),
    strength = if_else(between, 1, rep(c(2, 3, 4, 3, 5), length.out = n()))
  ) %>%
  left_join(community_nodes %>% select(from = id, x_from = x, y_from = y), by = "from") %>%
  left_join(community_nodes %>% select(to = id, x_to = x, y_to = y), by = "to")

base_network <- ggplot() +
  geom_segment(
    data = community_edges,
    aes(x = x_from, y = y_from, xend = x_to, yend = y_to, linewidth = strength),
    color = "#A8AFB8", alpha = .68
  ) +
  scale_linewidth(range = c(.45, 2.1), guide = "none") +
  coord_equal(xlim = c(-3.4, 3.4), ylim = c(-1.75, 1.75), clip = "off") +
  theme_void(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 21, color = "#18212B", margin = margin(b = 6)),
    plot.subtitle = element_text(size = 13, color = "#5B6570", margin = margin(b = 10)),
    plot.caption = element_text(size = 12.5, color = "#2D333A", face = "bold", hjust = .5, margin = margin(t = 8)),
    plot.margin = margin(18, 28, 18, 28),
    plot.background = element_rect(fill = "#FAFBFC", color = NA)
  )

p_network <- base_network +
  geom_point(
    data = community_nodes, aes(x, y),
    shape = 21, fill = "#73808C", color = "white", stroke = .8, size = 6
  ) +
  annotate("text", x = -1.9, y = 1.48, label = "Dense community", fontface = "bold", size = 5, color = "#2D333A") +
  annotate("text", x = 1.9, y = 1.48, label = "Dense community", fontface = "bold", size = 5, color = "#2D333A") +
  annotate("segment", x = -.62, xend = .62, y = -1.42, yend = -1.42,
           color = "#69737E", linewidth = .8) +
  annotate("text", x = 0, y = -1.62, label = "Few between-community ties", size = 4.3, color = "#2D333A") +
  labs(
    title = "Step 1 — Describe the network pattern",
    subtitle = "Edges are social-media connections • thicker edges indicate stronger connections",
    caption = "Network claim: the connections form two communities."
  )

p_interpreted <- base_network +
  geom_point(
    data = community_nodes,
    aes(x, y, fill = ideology), shape = 21, color = "white", stroke = .8, size = 6
  ) +
  annotate("text", x = -1.9, y = 1.48, label = "Mostly progressive\npolitical follows",
           fontface = "bold", lineheight = .95, size = 4.7, color = "#4C78A8") +
  annotate("text", x = 1.9, y = 1.48, label = "Mostly conservative\npolitical follows",
           fontface = "bold", lineheight = .95, size = 4.7, color = "#E45756") +
  scale_fill_manual(values = c(
    "Mostly progressive political follows" = "#4C78A8",
    "Mostly conservative political follows" = "#E45756"
  )) +
  guides(fill = "none") +
  labs(
    title = "Step 2 — Interpret the communities with external evidence",
    subtitle = "Political-following behavior is used to characterize—not discover—the social-media communities",
    caption = "Interpretive claim: the two network communities also differ in their members' political-following patterns."
  )

ggsave(
  "assets/network-communities.png", p_network,
  width = 13.5, height = 7.6, units = "in", dpi = 180, bg = "#FAFBFC"
)

ggsave(
  "assets/network-communities-interpreted.png", p_interpreted,
  width = 13.5, height = 7.6, units = "in", dpi = 180, bg = "#FAFBFC"
)
