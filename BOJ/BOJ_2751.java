import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		int cnt = Integer.parseInt(br.readLine());

		List<Integer> intList = new ArrayList<>();

		while (cnt-- > 0) {
			intList.add(Integer.parseInt(br.readLine()));
		}

		Collections.sort(intList);

		for (int i = 0; i < intList.size(); i++) {
			if (i == intList.size() - 1) {
				bw.write(intList.get(i) + "");
			} else {
				bw.write(intList.get(i) + "\n");
			}
		}

		bw.flush();
		bw.close();

	}

}
