library(tidyverse)

results_cpu <- read_csv('./results_cpu.csv') %>% rename(obs=X1, nb=nk)
results_jit <- read_csv('./results_jit.csv') %>% rename(obs=X1, nb=nk)
results_gpu <- read_csv('./results_gpu.csv') %>% rename(obs=X1, nb=nk)

master <- bind_rows(results_cpu, results_jit, results_gpu)

table <- master %>%
  spread(key='target', value='time') %>%
  select(obs, nb, cpu, jit, gpu)

statistics <- master %>%
  mutate(time = na_if(time, 0)) %>%
  group_by(target, nb) %>%
  summarize(
    avg_time = mean(time, na.rm=TRUE),
    std_time = sd(time, na.rm=TRUE),
    min_time = min(time, na.rm=TRUE),
    q25_time = quantile(time, 0.25, na.rm=TRUE),
    q50_time = quantile(time, 0.50, na.rm=TRUE),
    q75_time = quantile(time, 0.75, na.rm=TRUE),
    max_time = max(time, na.rm=TRUE)
  )

statistics %>% ggplot(aes(x=nb)) +
  geom_ribbon(aes(ymin=min_time, ymax=max_time, fill=target), alpha=0.3) +
  geom_line(aes(y=avg_time, color=target)) +
  labs(color="Function", fill="Function") +
  xlab('Number of gridpoints on state space') +
  ylab('VFI time (seconds)')
ggsave('./slides/img/benchmarks.pdf', width=20, height=8, units='cm')

statistics %>% ggplot(aes(x=nb)) +
  geom_ribbon(aes(ymin=min_time, ymax=max_time, fill=target), alpha=0.3) +
  geom_line(aes(y=avg_time, color=target)) +
  coord_trans(y='log10') +
  labs(color="Function", fill="Function") +
  xlab('Number of gridpoints on state space') +
  ylab('VFI time (seconds, log scale)')
ggsave('./slides/img/benchmarks-logscale.pdf', width=20, height=8, units='cm')

# statistics %>%
#   filter(nb == 100 | nb == 1000) %>%
#   arrange(nb, desc(target)) %>%
#   as.data.frame() %>%
#   stargazer::stargazer(out='./summary_results.tex', type='text', align=TRUE,
#                        summary=FALSE, rownames=FALSE, digits=5)
