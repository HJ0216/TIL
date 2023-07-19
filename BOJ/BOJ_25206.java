import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		Map<String, Double> score = new HashMap<>();
		score.put("A+", 4.5);
		score.put("A0", 4.0);
		score.put("B+", 3.5);
		score.put("B0", 3.0);
		score.put("C+", 2.5);
		score.put("C0", 2.0);
		score.put("D+", 1.5);
		score.put("D0", 1.0);
		score.put("F", 0.0);

		double total = 0;
		double d = 0;
		for (int i = 0; i < 20; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine());

			String[] strArr = new String[3];
			strArr[0] = st.nextToken();
			strArr[1] = st.nextToken();
			strArr[2] = st.nextToken();

			if (!strArr[2].equals("P")) {
				total += Double.valueOf(strArr[1]) * score.get(strArr[2]);
				d += Double.valueOf(strArr[1]);
			}

		}

		bw.write(total/d + "");

		bw.flush();
		bw.close();

	}

}
