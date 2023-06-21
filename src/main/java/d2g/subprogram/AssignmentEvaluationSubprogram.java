package d2g.subprogram;

import d2g.UserArguments;
import d2g.configuration.AssignmentConfiguration;
import d2g.configuration.TaskConfiguration;

import net.sourceforge.argparse4j.inf.Subparser;

import java.io.FileNotFoundException;

public class AssignmentEvaluationSubprogram extends Subprogram {
    public AssignmentEvaluationSubprogram() {
        super("eval");
    }

    @Override
    public boolean run() {
        AssignmentConfiguration config =
                loadAssignmentConfiguration(UserArguments.getString("assignment"));

        System.out.println(config);
        for (TaskConfiguration t : config.getTasks()) {
            System.out.println(t);
        }
        return true;
    }

    private AssignmentConfiguration loadAssignmentConfiguration(String path) {
        try {
            return AssignmentConfiguration.loadFromFile(path);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e); // TODO
        }
    }

    @Override
    protected void initSubparser(Subparser parser) {
        parser.addArgument("--assignment").setDefault("./").help("Assignment path");
    }
}
