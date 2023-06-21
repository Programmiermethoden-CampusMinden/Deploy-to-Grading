package d2g.configuration;

import d2g.configuration.metric.MetricConfiguration;
import d2g.utils.yaml.YamlHelper;
import d2g.utils.yaml.YamlKeys;

import org.yaml.snakeyaml.Yaml;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/** Java representation for a task.yml file */
public class TaskConfiguration {
    private static final Logger LOGGER = Logger.getLogger(TaskConfiguration.class.getName());

    private String name;
    private String description;
    private Map<String, MetricConfiguration> metrics;
    private List<String> noOverride;

    private TaskConfiguration() {}

    /**
     * Loads a task configuration from the given path.
     *
     * <p>The path must link to a folder containing a task.yml.
     *
     * @param path path to the task folder
     * @return fully loaded assignment configuration
     * @throws FileNotFoundException when a task.yml file could not be found
     */
    public static TaskConfiguration load(String path) throws FileNotFoundException {
        return load(new FileInputStream(path + "/task.yml"));
    }

    /**
     * Loads a task configuration from the given YAML input stream.
     *
     * @param stream Stream containing YAML data
     * @return fully loaded assignment configuration
     */
    public static TaskConfiguration load(InputStream stream) {
        Yaml yamlLoader = new Yaml();
        Map<String, Object> yaml = yamlLoader.load(stream);

        TaskConfiguration config = new TaskConfiguration();
        config.name = YamlHelper.getString(YamlKeys.NAME, yaml);
        config.description = YamlHelper.getString(YamlKeys.DESCRIPTION, yaml);

        config.noOverride = YamlHelper.getStringList(YamlKeys.NO_OVERRIDE, yaml);

        Map<String, Object> metricsYaml = YamlHelper.getYamlObject(YamlKeys.METRICS, yaml);
        if (metricsYaml != null) {
            config.metrics = new HashMap<>();
            for (String metric : metricsYaml.keySet()) {
                MetricConfiguration metricConfig =
                        MetricConfiguration.createFromYaml(
                                metric, YamlHelper.getYamlObject(metric, metricsYaml));
                if (metricConfig != null) config.metrics.put(metric, metricConfig);
            }
        }

        LOGGER.info(String.format("Loaded task with name %s", config.name));
        return config;
    }

    public String name() {
        return name;
    }

    /**
     * Creates a YAML description of the task configuration.
     *
     * <p>Currently only used for testing.
     *
     * @return task configuration as yaml string
     */
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append(String.format("%s: %s\n", YamlKeys.NAME, name));
        builder.append(
                String.format(
                        "%s: %s\n",
                        YamlKeys.DESCRIPTION,
                        description)); // TODO: Multiline string support required?

        if (metrics.size() > 0) {
            builder.append(String.format("%s:\n", YamlKeys.METRICS));
            for (String key : metrics.keySet()) {
                builder.append(metrics.get(key));
            }
        }

        if (noOverride.size() > 0) {
            builder.append(String.format("%s:\n", YamlKeys.NO_OVERRIDE));
            for (String s : noOverride) builder.append(String.format("- %s\n", s));
        }

        return builder.toString();
    }
}
