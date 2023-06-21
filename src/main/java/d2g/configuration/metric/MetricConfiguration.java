package d2g.configuration.metric;

import d2g.utils.yaml.YamlHelper;
import d2g.utils.yaml.YamlKeys;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

public abstract class MetricConfiguration {
    private static final Logger LOGGER = Logger.getLogger(MetricConfiguration.class.getName());

    private static Map<String, Class<? extends MetricConfiguration>> metricConfigurationClasses;

    /**
     * Register a new MetricConfiguration subclass with the given name.
     *
     * <p>This method returns false, when a metric configuration class with the given name already
     * exists or the class does not implement a createFromYaml method.
     *
     * <p>When creating a new metric class, make sure that it implements the createFromYaml method
     * that calls {@link #parseYaml(Map)} and that it calls the super constructor.
     *
     * @param name metric name
     * @param klass class inheriting from {@link MetricConfiguration}
     * @return registration success
     */
    public static boolean addMetricConfigurationClass(
            String name, Class<? extends MetricConfiguration> klass) {
        if (metricConfigurationClasses == null) metricConfigurationClasses = new HashMap<>();

        if (metricConfigurationClasses.containsKey(name)) {
            LOGGER.warning(
                    String.format("Tried to register metric configuration class %s twice", name));
            return false;
        }

        try {
            klass.getMethod("createFromYaml", Map.class);

            metricConfigurationClasses.put(name, klass);
        } catch (NoSuchMethodException e) {
            LOGGER.warning(
                    "Tried to register class that does not implement a createFromYaml method");
            return false;
        }
        return true;
    }

    /**
     * Creates a new metric configuration object using the given yaml data.
     *
     * <p>The metric configuration subclass used for creation is determined by the given name.
     *
     * <p>Returns null if no metric with the given name was registered or the metric configuration
     * can not be loaded.
     *
     * @param name metric name
     * @param data yaml data
     * @return metric configuration object of the determined type
     */
    public static MetricConfiguration createFromYaml(String name, Map<String, Object> data) {
        if (!metricConfigurationClasses.containsKey(name)) {
            LOGGER.warning(
                    String.format(
                            "Tried to create metric configuration for unknown metric %s", name));
            return null;
        }

        try {
            return (MetricConfiguration)
                    metricConfigurationClasses
                            .get(name)
                            .getMethod("createFromYaml", Map.class)
                            .invoke(null, data); // TODO
        } catch (NoSuchMethodException | InvocationTargetException | IllegalAccessException e) {
            return null;
        }
    }

    protected ScoringStrategy scoringStrategy;
    protected Integer points;

    /** List of metrics that need to be successfully executed prior to this metric. */
    protected List<String> dependsOn;

    protected MetricConfiguration() {
        dependsOn = new ArrayList<>();
    }

    /**
     * Parses YAML data shared between all metric configurations.
     *
     * <p>The parsed YAML data are the scoring strategy and the list of metrics, on which the
     * current metric depends on.
     *
     * @param data yaml data
     */
    protected void parseYaml(Map<String, Object> data) {
        if (data.containsKey(YamlKeys.POINTS)) {
            scoringStrategy = ScoringStrategy.FIXED;
            points = YamlHelper.getInt(YamlKeys.POINTS, data);
        } else if (data.containsKey(YamlKeys.MAX_POINTS)) {
            scoringStrategy = ScoringStrategy.PER_MISTAKE;
            points = YamlHelper.getInt(YamlKeys.MAX_POINTS, data);
        } else if (data.containsKey(YamlKeys.POINTS_PER_TEST)) {
            scoringStrategy = ScoringStrategy.PER_TEST;
            points = YamlHelper.getInt(YamlKeys.POINTS_PER_TEST, data);
        } else {
            // TODO: Does this need an error message or can we assume that nothing means custom
            // strategy?
            scoringStrategy = ScoringStrategy.CUSTOM;
            points = 0;
        }

        if (data.containsKey(YamlKeys.DEPENDS_ON))
            this.dependsOn =
                    YamlHelper.getStringList(
                            YamlKeys.DEPENDS_ON,
                            data); // TODO: Fails when used as a single string instead of list
    }
}
