package d2g.utils.yaml;

import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/** Helper class containing static methods for parsing yaml configuration files. */
public class YamlHelper {
    private static final Logger LOGGER = Logger.getLogger(YamlHelper.class.getName());

    /**
     * Get string data from yaml object.
     *
     * @param key YAML attribute name
     * @param data YAML data object
     * @return
     */
    public static String getString(String key, Map<String, Object> data) {
        if (!data.containsKey(key))
            return logErrorAndReturnString(String.format("Unknown key %s", key));
        if (!(data.get(key) instanceof String))
            return logErrorAndReturnString(String.format("Key %s is not a string", key));

        if (data.get(key) == null) LOGGER.warning(String.format("Key %s is null", key));
        return (String) data.get(key);
    }

    public static Integer getInt(String key, Map<String, Object> data) {
        if (!data.containsKey(key)) {
            logError(String.format("Unknown key %s", key));
            return null;
        }

        if (!(data.get(key) instanceof Integer)) {
            logError(String.format("Key %s is not an int", key));
            return null;
        }

        if (data.get(key) == null) LOGGER.warning(String.format("Key %s is null", key));
        return (Integer) data.get(key);
    }

    public static LocalDateTime getDate(String key, Map<String, Object> data) {
        String s = getString(key, data);

        if (s == null) return null;

        try {
            return LocalDateTime.parse(s);
        } catch (DateTimeParseException e) {
            logError(String.format("Invalid date format at key %s", key));
            return null;
        }
    }

    public static List<?> getList(String key, Map<String, Object> data) {
        if (!data.containsKey(key)) {
            logError(String.format("Unknown key %s", key));
            return null;
        }

        if (!(data.get(key) instanceof List<?>)) {
            logError(String.format("Key %s is not a list", key));
            return null;
        }

        return (List<?>) data.get(key);
    }

    public static int getListSize(String key, Map<String, Object> data) {
        List<?> list = getList(key, data);

        if (list == null) return 0; // TODO: Or should -1 be returned?
        return list.size();
    }

    public static List<String> getStringList(String key, Map<String, Object> data) {
        List<?> list = getList(key, data);

        if (list == null) return null;

        List<String> stringList = new ArrayList<>(list.size());
        for (Object obj : list) {
            if (!(obj instanceof String))
                logError(String.format("Found obj that is not of type String in list %s", key));
            else stringList.add((String) obj);
        }

        if (stringList.size() == 0) return null;
        return stringList;
    }

    public static Map<String, Object> getYamlObject(String key, Map<String, Object> data) {
        if (!data.containsKey(key)) {
            logError(String.format("Unknown key %s", key));
            return null;
        }
        if (!(data.get(key) instanceof Map)) {
            logError(String.format("Key %s is not a yaml Object", key));
            return null;
        }

        return (Map<String, Object>) data.get(key); // TODO
    }

    private static void logError(String msg) {
        LOGGER.warning(String.format("[Yaml Error] %s", msg));
    }

    private static String logErrorAndReturnString(String msg) {
        logError(msg);
        return null;
    }
}
