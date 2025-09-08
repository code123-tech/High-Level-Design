package Questions.Bloom_Filter;

import java.util.BitSet;

public class BloomFilterImplementation {

    private final BitSet bitSetArray;
    private final int m; // Size of the bit set array
    private final int k; // Number of hash functions
    
    /**
     * n - number of expected elements
     * p - probability of false positives
     * below formulas are standard one, can read: 
     * <a href="BasicConcepts/Bloom_Filters/README.md">Bloom Filters</a>
     */
    public BloomFilterImplementation(int n, double p) {

        this.m = (int) Math.ceil(-(n * Math.log(p)) / Math.pow(Math.log(2), 2));
        this.k = Math.max(1, (int) Math.ceil((m / (double) n) * Math.log(2)));
        this.bitSetArray = new BitSet(m);
    }

    public void addElement(String item) {

        for(int index: getKHashes(item)) {
            bitSetArray.set(index);
        }
    }

    public boolean checkItemExist(String item) {

        for(int index: getKHashes(item)) {
            if(!bitSetArray.get(index)) {
                return false;
            }
        }
        return true;
    }

    private int[] getKHashes(String item) {
        int[] hashes = new int[k];

        int h1 = smear(item.hashCode());
        int h2 = smear(item.hashCode() * 0x9e3779b9); // golden ratio constant to decorrelate
        if (h2 == 0) h2 = 1;

        for (int i = 0; i < k; i++) {
            long combined = (long) h1 + (long) i * (long) h2;
            int index = (int) ((combined & 0x7fffffffL) % m);
            hashes[i] = index;
        }
        return hashes;
    }

    private static int smear(int x) {
        // Let's explain each line of the smear function with an example.
        // Suppose x = 123456789

        // 1. x ^= (x >>> 16);
        //    - ">>> 16" means shift x right by 16 bits, filling with zeros.
        //    - x = 123456789 = 0x075BCD15
        //    - x >>> 16 = 0x0000075B = 1883
        //    - x ^ 1883 = 123456789 ^ 1883 = 123458600
        //    - Now x = 123458600

        // 2. x *= 0x7feb352d;
        //    - 0x7feb352d = 2146434349
        //    - x = 123458600 * 2146434349 = 264997964964124140
        //    - Now x = 264997964964124140

        // 3. x ^= (x >>> 15);
        //    - x >>> 15 = 264997964964124140 >>> 15 = 8090739640
        //    - x ^ 8090739640 = 264997964964124140 ^ 8090739640 = 264997957873384508
        //    - Now x = 264997957873384508

        // 4. x *= 0x846ca68b;
        //    - 0x846ca68b = 2229579579
        //    - x = 264997957873384508 * 2229579579 = 590944393964375964234222332
        //    - Now x = 590944393964375964234222332

        // 5. x ^= (x >>> 16);
        //    - x >>> 16 = 590944393964375964234222332 >>> 16 = 9020739643939642342
        //    - x ^ 9020739643939642342 = 590944393964375964234222332 ^ 9020739643939642342 = 590944393955355224590289990
        //    - Now x = 590944393955355224590289990

        // 6. return x;
        //    - The final value is returned.

        // In summary, each line mixes the bits of x using bitwise XOR and multiplication with large constants.
        // This helps to "smear" the bits, producing a more uniform and unpredictable hash value.
        x ^= (x >>> 16);
        x *= 0x7feb352d;
        x ^= (x >>> 15);
        x *= 0x846ca68b;
        x ^= (x >>> 16);
        return x;
    }


    public static void main(String[] args) {
        
        BloomFilterImplementation bloomFilter = new BloomFilterImplementation(1000, 0.01);
        bloomFilter.addElement("apple");
        System.out.println("Element 'apple' added to bloom filter");
        bloomFilter.addElement("banana");
        System.out.println("Element 'banana' added to bloom filter");

        System.out.println("Is apple present? " + bloomFilter.checkItemExist("apple"));
        System.out.println("Is banana present? " + bloomFilter.checkItemExist("banana"));
        System.out.println("Is orange present? " + bloomFilter.checkItemExist("orange"));
    }

}
