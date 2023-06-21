package d2g.configuration.metric;

import d2g.utils.yaml.YamlKeys;

import java.util.Map;
import java.util.logging.Logger;

public class CompileMetricConfiguration extends MetricConfiguration {
    private static final Logger LOGGER =
            Logger.getLogger(CompileMetricConfiguration.class.getName());

    /*static {
        MetricConfiguration.addMetricConfigurationClass(
                "compile", CompileMetricConfiguration.class);
    }*/
    // TODO: Why does this not work?

    public static MetricConfiguration createFromYaml(Map<String, Object> data) {
        CompileMetricConfiguration config = new CompileMetricConfiguration();
        config.parseYaml(data);

        if (config.scoringStrategy != ScoringStrategy.FIXED) {
            LOGGER.warning(
                    "compile metric configured with wrong scoring strategy. Setting it to 'fixed'");
            config.scoringStrategy = ScoringStrategy.FIXED;
        }

        return config;
    }

    /**
     * Creates a YAML description of the compile metric configuration.
     *
     * <p>Currently only used for testing.
     *
     * @return compile metric configuration as yaml string
     */
    public String toString() {

        StringBuilder builder = new StringBuilder();
        builder.append(String.format("  %s:\n", YamlKeys.COMPILE));
        builder.append(String.format("    %s: %d\n", YamlKeys.POINTS, points));

        if (dependsOn.size() > 0) {
            builder.append(String.format("    %s:\n", YamlKeys.DEPENDS_ON));
            for (String s : dependsOn) builder.append(String.format("    - %s\n", s));
        }

        return builder.toString();
    }
}
