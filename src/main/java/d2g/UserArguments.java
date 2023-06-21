package d2g;

import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.Namespace;
import net.sourceforge.argparse4j.inf.Subparser;
import net.sourceforge.argparse4j.inf.Subparsers;

public class UserArguments {

    private static final int SUBPROGRAM_NAME_INDEX = 0;

    private static UserArguments obj;

    public static String getString(String key) {
        if (obj == null || obj.settings == null) return null;
        return obj.settings.get(key);
    }

    public static String getSelectedSubprogramName() {
        if (obj == null || obj.settings == null) return null;
        return obj.subprogramName;
    }

    public static UserArguments get() {
        if (obj == null) obj = new UserArguments();
        return obj;
    }

    private ArgumentParser mainParser;
    private Subparsers subparsers;

    private Namespace settings;
    private String subprogramName;

    private UserArguments() {
        mainParser =
                ArgumentParsers.newFor("d2g").build().description("Deploy-to-Grading Toolchain");

        subparsers = mainParser.addSubparsers();
    }

    public void parseArgs(String[] args) {
        if (args.length > SUBPROGRAM_NAME_INDEX)
            // TODO: Make sure that only valid subprogram names are set and options are ignored
            // TODO: Maybe not make it based on position but count the number of words that are not
            // option related
            subprogramName = args[SUBPROGRAM_NAME_INDEX];

        settings = mainParser.parseArgsOrFail(args);
    }

    public Subparser createSubparser(String name) {
        return subparsers.addParser(name);
    }
}
