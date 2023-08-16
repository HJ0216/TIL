import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int N = Integer.parseInt(br.readLine());

		Map<Integer, ArrayList<String>> listMap = new HashMap<>();

		for (int i = 0; i < N; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine());
			int age = Integer.parseInt(st.nextToken());
			String name = st.nextToken();

			if (!listMap.containsKey(age)) {
				listMap.put(age, new ArrayList<>());
			}

			listMap.get(age).add(name);

		}

		Object[] mapKeys = listMap.keySet().toArray();
		Arrays.sort(mapKeys);

		for (Object key : mapKeys) {
			for (String s : listMap.get(key)) {
				bw.write(key + " " + s + "\n");
			}
		}

		bw.flush();
		bw.close();
	}

}
