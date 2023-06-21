package d2g.subprogram;

import d2g.UserArguments;

import net.sourceforge.argparse4j.inf.Subparser;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

public abstract class Subprogram {
    private static final Logger LOGGER = Logger.getLogger(Subprogram.class.getName());

    private static Map<String, Subprogram> subprograms;

    public static boolean runSubprogram(String name) {
        if (subprograms == null || !subprograms.containsKey(name)) {
            LOGGER.severe(String.format("Unknown subprogram %s", name));
            return false;
        }

        return subprograms.get(name).run();
    }

    private boolean registerSubprogram(String name) {
        if (subprograms == null) subprograms = new HashMap<>();

        if (subprograms.containsKey(name)) {
            LOGGER.warning(String.format("Tried to register subprogram %s twice", name));
            return false;
        }

        subprograms.put(name, this);
        initSubparser(UserArguments.get().createSubparser(name));

        LOGGER.info(String.format("Registered subprogram %s", name));
        return true;
    }

    protected Subprogram(String name) {
        registerSubprogram(name);
    }

    public abstract boolean run();

    protected abstract void initSubparser(Subparser parser);
}
