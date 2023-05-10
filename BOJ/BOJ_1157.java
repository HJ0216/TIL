import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		String s = br.readLine().toLowerCase();

	    int[] alphabet = new int[26];

	    for (int i = 0; i < s.length(); i++) {
	        char c = s.charAt(i);
	        alphabet[c - 'a']++;
	    }

	    int maxCount = 0;
	    char result = '?';

	    for (int i = 0; i < 26; i++) {
	        if (alphabet[i] > maxCount) {
	            maxCount = alphabet[i];
	            result = (char) (i + 'A');
	        } else if (alphabet[i] == maxCount) {
	            result = '?';
	        }
	    }
	    

	    bw.write(result);
	    
		bw.flush();
		bw.close();
	}
}
