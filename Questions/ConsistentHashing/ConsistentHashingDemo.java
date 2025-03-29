package Questions.ConsistentHashing;

import java.util.HashMap;

import java.util.Map;

public class ConsistentHashingDemo {
    
    public static void main(String[] args){

        ConsistentHashing consistentHashing = new ConsistentHashing(100);

        consistentHashing.addNode("Node1");
        consistentHashing.addNode("Node2");
        consistentHashing.addNode("Node3");
        consistentHashing.addNode("Node4");
        consistentHashing.addNode("Node5");
        
        Map<String, Integer> nodeCount = new HashMap<>();
        int requests = 1000000;

        for(int i = 0; i < requests; i++) {

            String key = "request-" + i;
            String node = consistentHashing.getNode(key);
            if(node == null){
                continue;
            }

            nodeCount.put(node, nodeCount.getOrDefault(node, 0) + 1);

        }

        System.out.println("Printing node count");
        for(Map.Entry<String, Integer> entry : nodeCount.entrySet()) {
            System.out.println(entry.getKey() + " : " + entry.getValue());
        }
    }

}
