using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class SofaAgent : Agent
{
    const int RIGHT = 1;
    const int LEFT = 2;
    const int UP = 3;
    const int DOWN = 4;

    const int BEDXSIZE = 2;
    const int BEDZSIZE = 4;
    const int SOFAXSIZE = 4;
    const int SOFAZSIZE = 2;

    public Map map;
    public Transform Bed;
    public FurnitureBedAgent bedAgent;
    public Color sofaMapColor;

    private float closeWallPositionZ = -11f;
    private float playerDistance = 0f;

    private float alpha;

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(closeWallPositionZ);

        sensor.AddObservation(transform.position);
        sensor.AddObservation(Bed.position);

        sensor.AddObservation(Mathf.Abs(Mathf.Abs(transform.position.z) - closeWallPositionZ));

        sensor.AddObservation(getManhattanDistance(Bed.position, transform.position));
        sensor.AddObservation(playerDistance);
    }

    public override void CollectDiscreteActionMasks(DiscreteActionMasker actionMasker)
    {
        int x = (int)transform.position.x;
        int z = (int)transform.position.z;

        map.deleteMap(x, z * -1, SOFAXSIZE, SOFAZSIZE);

        if (transform.position.x >= 7.5f || !map.canFillMap(x + 1, z * -1, SOFAXSIZE, SOFAZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { RIGHT });
        }

        else if (transform.position.x <= 0.5f || !map.canFillMap(x - 1, z * -1, SOFAXSIZE, SOFAZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { LEFT });
        }

        if (transform.position.z >= -0.5f || !map.canFillMap(x, (z + 1) * -1, SOFAXSIZE, SOFAZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { UP });
        }

        else if (transform.position.z <= -9.5f || !map.canFillMap(x, (z - 1) * -1, SOFAXSIZE, SOFAZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { DOWN });
        }

        map.fillMap(x, z * -1, SOFAXSIZE, SOFAZSIZE, sofaMapColor);
    }

    private float getManhattanDistance(Vector3 from, Vector3 to)
    {
        float xDistance = Mathf.Abs(to.x - from.x);
        float zDistance = Mathf.Abs(to.z - from.z);

        return xDistance + zDistance;
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        alpha = bedAgent.alpha;

        float action = vectorAction[0];

        int x = (int)transform.position.x;
        int z = (int)transform.position.z;

        map.deleteMap(x, z * -1, SOFAXSIZE, SOFAZSIZE);
        
        switch (action)
        {
            case 0:
                break;
            case RIGHT:
                if(x <= 7.5f) transform.position = new Vector3(x + 1, 0, z);
                break;
            case LEFT:                
                if(x >= 0.5f) transform.position = new Vector3(x - 1, 0, z);
                break;
            case UP:
                if(z <= -0.5f) transform.position = new Vector3(x, 0, z + 1);
                break;
            case DOWN:                
                if(z >= -9.5f) transform.position = new Vector3(x, 0, z - 1);
                break;
            default:
                break;
        }

        x = (int)transform.position.x;
        z = (int)transform.position.z;

        map.fillMap(x, z * -1, SOFAXSIZE, SOFAZSIZE, sofaMapColor);

        playerDistance = getDistance();
        bedAgent.playerDistance = playerDistance;

        AddReward(getReward());
        bedAgent.AddReward(bedAgent.getReward());

        bedAgent.RequestDecision();
    }

    private float getDistance()
    {
        float distance = 0;

        distance += getManhattanDistance(Bed.position, transform.position);

        return distance;
    }

    private float getReward()
    {
        float distance = Mathf.Abs(closeWallPositionZ - transform.position.z);
        float reward = -((1 - alpha) * distance) - (alpha * playerDistance);

        return reward;
    }
}
