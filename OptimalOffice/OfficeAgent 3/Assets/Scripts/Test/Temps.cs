using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Temps : MonoBehaviour
{
    /*const int RIGHT = 1;
    const int LEFT = 2;
    const int UP = 3;
    const int DOWN = 4;

    const int BEDXSIZE = 2;
    const int BEDZSIZE = 4;
    const int SOFAXSIZE = 4;
    const int SOFAZSIZE = 2;

    public Transform Sofa;
    public Transform window, playerStartTransform;
    public List<Transform> corners;
    public Map map;
    public Color bedMapColor, sofaMapColor;

    private Transform cornerMinTransform;

    public SofaAgent sofaAgent;

    public float alpha = 0.1f;

    int cnt = 0;

    string result = "";

    [HideInInspector]
    public float playerDistance = 0f;

    int episode = 0;

    public override void OnEpisodeBegin()
    {
        Debug.Log("Episode: " + cnt);

        episode = 0;
        map.clearMap();
        cornerMinTransform = corners[0];

        //Bed Random Batch
        int x = Random.Range(0, 11);
        int z = Random.Range(-8, 1);

        transform.position = new Vector3(x, 0, z);
        map.fillMap(x, z * -1, BEDXSIZE, BEDZSIZE, bedMapColor);

        while (true)
        {
            //Sofa Random Batch
            x = Random.Range(0, 9);
            z = Random.Range(-10, 1);

            Sofa.position = new Vector3(x, 0, z);

            if (map.canFillMap(x, z * -1, SOFAXSIZE, SOFAZSIZE))
            {
                map.fillMap(x, z * -1, SOFAXSIZE, SOFAZSIZE, sofaMapColor);
                break;
            }
        }
    }

    public override void CollectDiscreteActionMasks(DiscreteActionMasker actionMasker)
    {
        int x = (int)transform.position.x;
        int z = (int)transform.position.z;

        map.deleteMap(x, z * -1, BEDXSIZE, BEDZSIZE);

        if (transform.position.x >= 9.5f || !map.canFillMap(x + 1, z * -1, BEDXSIZE, BEDZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { RIGHT });
        }

        else if (transform.position.x <= 0.5f || !map.canFillMap(x - 1, z * -1, BEDXSIZE, BEDZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { LEFT });
        }

        if (transform.position.z >= -0.5f || !map.canFillMap(x, (z + 1) * -1, BEDXSIZE, BEDZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { UP });
        }

        else if (transform.position.z <= -7.5f || !map.canFillMap(x, (z - 1) * -1, BEDXSIZE, BEDZSIZE))
        {
            actionMasker.SetMask(0, new int[1] { DOWN });
        }

        map.fillMap(x, z * -1, BEDXSIZE, BEDZSIZE, bedMapColor);
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        for (var i = 0; i < 4; i++)
        {
            sensor.AddObservation(corners[i].position);
        }

        sensor.AddObservation(transform.position);
        sensor.AddObservation(Sofa.position);
        sensor.AddObservation(window.position);

        sensor.AddObservation(Vector3.Distance(cornerMinTransform.position, transform.position));
        sensor.AddObservation(Vector3.Distance(window.position, transform.position));

        sensor.AddObservation(getManhattanDistance(transform.position, Sofa.position));
        sensor.AddObservation(playerDistance);
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        episode += 1;

        float action = vectorAction[0];

        int x = (int)transform.position.x;
        int z = (int)transform.position.z;

        map.deleteMap(x, z * -1, BEDXSIZE, BEDZSIZE);

        switch (action)
        {
            case 0:
                break;
            case RIGHT:
                if (x <= 9.5f) transform.position = new Vector3(x + 1, 0, z);
                break;
            case LEFT:
                if (x >= 0.5f) transform.position = new Vector3(x - 1, 0, z);
                break;
            case UP:
                if (z <= -0.5f) transform.position = new Vector3(x, 0, z + 1);
                break;
            case DOWN:
                if (z >= -7.5f) transform.position = new Vector3(x, 0, z - 1);
                break;
            default:
                break;
        }

        x = (int)transform.position.x;
        z = (int)transform.position.z;

        map.fillMap(x, z * -1, BEDXSIZE, BEDZSIZE, bedMapColor);

        findCloseCorner();

        if (episode >= 2000)
        {
            cnt += 1;

            Debug.Log("Bed: " + GetCumulativeReward() + "\n" + "Sofa: " + sofaAgent.GetCumulativeReward());

            sofaAgent.EndEpisode();
            EndEpisode();
        }

        else
        {
            sofaAgent.RequestDecision();
        }
    }

    private float getManhattanDistance(Vector3 from, Vector3 to)
    {
        float xDistance = Mathf.Abs(to.x - from.x);
        float zDistance = Mathf.Abs(to.z - from.z);

        return xDistance + zDistance;
    }

    private void findCloseCorner()
    {
        float minDistance = 1000000;

        for (var i = 0; i < 4; i++)
        {
            float distance = Vector3.Distance(corners[i].position, transform.position);

            if (minDistance > distance)
            {
                cornerMinTransform = corners[i];
                minDistance = distance;
            }
        }
    }

    public float getReward()
    {
        float cornerDistance = Vector3.Distance(transform.position, cornerMinTransform.position);
        float windowDistance = Vector3.Distance(window.position, transform.position);

        float reward = -((1 - alpha) * (cornerDistance + windowDistance)) - (alpha * playerDistance);

        return reward;
    }*/
}
