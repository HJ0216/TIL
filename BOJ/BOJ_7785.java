import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int num = Integer.parseInt(br.readLine());

		Map<String, String> map = new HashMap<>();
		for (int i = 0; i < num; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine());
			String name = st.nextToken();
			String status = st.nextToken();

			if (!map.containsKey(name)) {
				map.put(name, status);
			} else {
				map.remove(name);
			}
		}

		List<String> keyList = new ArrayList<>(map.keySet());
		keyList.sort((s1, s2) -> s2.compareTo(s1));

		for (String s : keyList) {
			bw.write(s + "\n");
		}

		bw.flush();
		bw.close();
	}

}
