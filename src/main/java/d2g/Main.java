package d2g;

import d2g.configuration.metric.CompileMetricConfiguration;
import d2g.configuration.metric.MetricConfiguration;
import d2g.subprogram.AssignmentEvaluationSubprogram;
import d2g.subprogram.Subprogram;

public class Main {

    /**
     * Main function
     *
     * @param args user args
     */
    public static void main(String[] args) {
        initSubprograms();
        registerMetricConfigurations();
        UserArguments.get().parseArgs(args);

        Subprogram.runSubprogram(UserArguments.getSelectedSubprogramName());
    }

    private static void initSubprograms() {
        new AssignmentEvaluationSubprogram();
    }

    private static void registerMetricConfigurations() {
        // TODO: Replace this function with static stuff inside the actual classes
        // Possible solution: Use annotations
        // (https://stackoverflow.com/questions/13128552/how-to-scan-classes-for-annotations)
        MetricConfiguration.addMetricConfigurationClass(
                "compile", CompileMetricConfiguration.class);
    }
}
