import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int N = Integer.parseInt(br.readLine());

		Map<String, Integer> map = new HashMap<>();

		for (int i = 0; i < N; i++) {
			String s = br.readLine();
			map.put(s, s.length());
		}

		Object[] mapKeys = map.keySet().toArray();
		Arrays.sort(mapKeys);

		List<Object> keys = new ArrayList<>();
		for (Object key : mapKeys) {
			keys.add(key);
		}
		Collections.sort(keys, ((k1, k2) -> (map.get(k1).compareTo(map.get(k2)))));

		for (Object key : keys) {
			bw.write(key + "\n");
		}

		bw.flush();
		bw.close();
	}

}
