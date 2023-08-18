import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeSet;

public class Main {

	static Map<Long, Integer> map;

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int N = Integer.parseInt(br.readLine());

		Set<Long> set = new TreeSet<>();

		List<Long> list = new ArrayList<>();

		StringTokenizer st = new StringTokenizer(br.readLine());

		for (int i = 0; i < N; i++) {
			long num = Long.parseLong(st.nextToken());
			set.add(num);
			list.add(num);
		}

		map = new HashMap<>();

		int cnt = 0;
		for (Long l : set) {
			map.put(l, cnt++);
		}

		StringBuffer sb = new StringBuffer();

		for (int i = 0; i < N; i++) {
			sb.append(map.get(list.get(i)) + " ");
		}

		bw.write(sb + "");

		bw.flush();
		bw.close();
	}

}
