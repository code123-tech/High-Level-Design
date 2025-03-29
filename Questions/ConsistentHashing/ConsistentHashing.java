package Questions.ConsistentHashing;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Map;
import java.util.TreeMap;

public class ConsistentHashing {
    
    private final TreeMap<Long, String> hashRing = new TreeMap<>();
    private final int virtualNodes;
    private final MessageDigest sha256;

    public ConsistentHashing(int virtualNodes) {

        this.virtualNodes = virtualNodes;
        try {
            this.sha256 = MessageDigest.getInstance("SHA-256");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public long hashSHA256(String key) {

        if(this.sha256 == null) {
            throw new RuntimeException("SHA-256 is not available");
        }

        this.sha256.update(key.getBytes(StandardCharsets.UTF_8));
        
        byte[] digest = this.sha256.digest();
        return ((long) (digest[3] & 0xFF) << 24) | ((long) (digest[2] & 0xFF) << 16) | ((long) (digest[1] & 0xFF) << 8) | (digest[0] & 0xFF);
    }

    public void addNode(String node){
        for(int i = 0; i < this.virtualNodes; i++) {
            this.hashRing.put(this.hashSHA256(node + "#" + i), node);
        }
    }

    public void removeNode(String node){
        for(int i = 0; i < this.virtualNodes; i++) {
            this.hashRing.remove(this.hashSHA256(node + "#" + i));
        }
    }

    public String getNode(String key) {
        if(this.hashRing.isEmpty()) {
            return null;
        }

        long hash = this.hashSHA256(key);
        Map.Entry<Long, String> entry = this.hashRing.ceilingEntry(hash);
        if(entry == null) {
            entry = this.hashRing.firstEntry();
        }

        return entry.getValue();
    }

    public void printNodes(){
        System.out.println("Nodes in the hash ring are: " + new HashSet<>(this.hashRing.values()));
    }

}
