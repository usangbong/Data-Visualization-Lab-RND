using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class UpDownObjectMove : Agent
{
    float targetYpos;

    bool changePos;

    public override void CollectObservations()
    {
        AddVectorObs(targetYpos);
    }

    public override void AgentAction(float[] vectorAction)
    {
        if (!changePos)
        {
            targetYpos = Mathf.Round(Random.Range(0, 2.2f) * 100) * 0.01f;
            changePos = true;
        }

        transform.position = Vector3.MoveTowards(transform.position,
            new Vector3(transform.position.x, targetYpos, transform.position.z), 1.0f * Time.deltaTime);

        if (transform.position.y == targetYpos)
        {
            changePos = false;
        }
    }
}
