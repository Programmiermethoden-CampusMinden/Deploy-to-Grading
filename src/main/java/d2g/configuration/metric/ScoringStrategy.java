package d2g.configuration.metric;

public enum ScoringStrategy {

    /**
     * Defines a point scoring strategy with a fixed point count. Points are either given full or
     * none.
     *
     * <p>Required yaml field: points
     */
    FIXED,
    /**
     * Defines a point scoring strategy with deductions based on the number of errors.
     *
     * <p>Required yaml field: max_points
     */
    PER_MISTAKE,
    /**
     * Defines a point scoring strategy for multiple test cases with a fixed number of points per
     * test case. This is used when the number of test cases is unknown or can vary.
     *
     * <p>Required yaml field: points_per_test
     */
    PER_TEST,
    /**
     * Sets a custom point scoring strategy defined inside the metric itself. Used, for example, for
     * JGrade Unittests.
     */
    CUSTOM
}
