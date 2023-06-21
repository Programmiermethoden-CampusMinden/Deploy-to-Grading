package d2g.utils.yaml;

/** Helper class containing the names of all possible YAML attributes */
public class YamlKeys {

    /** General */
    public static final String NAME = "name";

    public static final String DESCRIPTION = "description";

    /** assignment.yml */
    public static final String DUE_DATE = "due_date";

    public static final String TASKS = "tasks";

    /** task.yml */
    public static final String METRICS = "metrics";

    public static final String NO_OVERRIDE = "no_override";

    /** Metrics */
    public static final String COMPILE = "compile";

    public static final String JUNIT = "junit";
    public static final String CHECKSTYLE = "checkstyle";

    /** Metric settings */
    public static final String POINTS = "points";

    public static final String MAX_POINTS = "max_points";
    public static final String POINTS_PER_TEST = "points_per_test";
    public static final String DEPENDS_ON = "depends_on";
}
