package d2g.configuration;

import d2g.utils.yaml.YamlHelper;
import d2g.utils.yaml.YamlKeys;

import org.yaml.snakeyaml.Yaml;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.logging.Logger;

/** Java representation for an assignment.yml file */
public class AssignmentConfiguration {
    private static final Logger LOGGER = Logger.getLogger(AssignmentConfiguration.class.getName());

    private String name;
    private String description;
    private LocalDateTime dueDate;
    private List<TaskConfiguration> tasks;

    private AssignmentConfiguration() {}

    /**
     * Loads an assignment configuration from the given path.
     *
     * <p>The path must link to a folder containing an assignment.yml.
     *
     * @param path path to the assignment folder
     * @return fully loaded assignment configuration
     * @throws FileNotFoundException when an assignment.yml file could not be found
     */
    public static AssignmentConfiguration loadFromFile(String path) throws FileNotFoundException {
        return load(path, new FileInputStream(path + "/assignment.yml"));
    }

    /**
     * Loads an assignment configuration from the given YAML input stream.
     *
     * <p>Also loads all tasks referenced in the assignment data. It looks for task yml files on the
     * path "<path>/<task>/task.yml"
     *
     * @param path path to the folder that contains the assignment.yml
     * @param stream Stream containing YAML data
     * @return fully loaded assignment configuration
     */
    public static AssignmentConfiguration load(String path, InputStream stream) {
        Yaml yamlLoader = new Yaml();
        Map<String, Object> yaml = yamlLoader.load(stream);

        AssignmentConfiguration config = new AssignmentConfiguration();
        config.name = YamlHelper.getString(YamlKeys.NAME, yaml);
        config.description = YamlHelper.getString(YamlKeys.DESCRIPTION, yaml);
        config.dueDate = YamlHelper.getDate(YamlKeys.DUE_DATE, yaml);

        int listSize = YamlHelper.getListSize(YamlKeys.TASKS, yaml);
        if (listSize > 0) {
            config.tasks = new ArrayList<>(listSize);
            for (Object task : Objects.requireNonNull(YamlHelper.getList(YamlKeys.TASKS, yaml))) {
                String taskPath = path + "/" + task;
                try {
                    config.tasks.add(TaskConfiguration.load(taskPath));
                } catch (FileNotFoundException e) {
                    LOGGER.severe(String.format("Configuration file for task %s not found", task));
                }
            }
        }

        LOGGER.info(String.format("Loaded assignment with name %s", config.name));
        return config;
    }

    public List<TaskConfiguration> getTasks() {
        return tasks;
    }

    /**
     * Creates a YAML description of the assignment configuration.
     *
     * <p>Currently only used for testing.
     *
     * @return assignment configuration as yaml string
     */
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append(String.format("%s: %s\n", YamlKeys.NAME, name));
        builder.append(
                String.format(
                        "%s: %s\n",
                        YamlKeys.DESCRIPTION,
                        description)); // TODO: Multiline string support required?
        builder.append(
                String.format(
                        "%s: %s\n",
                        YamlKeys.DUE_DATE,
                        dueDate.toString())); // TODO: Is return value format standardized?

        if (tasks.size() > 0) {
            builder.append(String.format("%s:\n", YamlKeys.TASKS));
            for (TaskConfiguration task : tasks)
                builder.append(String.format("- %s\n", task.name()));
        }

        return builder.toString();
    }
}
