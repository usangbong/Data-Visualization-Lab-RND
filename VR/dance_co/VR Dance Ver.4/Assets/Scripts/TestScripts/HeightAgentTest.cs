using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class HeightAgentTest : Agent
{
    public GameObject VRPlayer;

    public float moveForce;

    Rigidbody rigidBody;
    GameObject Head;

    void Awake()
    {
        Head = VRPlayer.transform.GetChild(0).gameObject;

        rigidBody = GetComponent<Rigidbody>();
    }

    public override void InitializeAgent()
    {
        rigidBody.velocity = Vector3.zero;

        ResetHead();
    }

    public override void CollectObservations()
    {
        AddVectorObs(Head.transform.position.y);
    }

    public override void AgentReset()
    {
        rigidBody.velocity = Vector3.zero;

        ResetHead();
    }

    void ResetHead()
    {
        Vector3 randomPos = new Vector3(Random.Range(-1.6f, 1.6f), Random.Range(0, 2f), Random.Range(-1.2f, 1.2f));
        Head.transform.position = randomPos;
    }

    public override void AgentAction(float[] vectorAction)
    {
        float horizontalInput = vectorAction[0];
        float verticalInput = vectorAction[1];
        float jumpInput = vectorAction[2];

        rigidBody.AddForce(horizontalInput * moveForce, jumpInput * moveForce, verticalInput * moveForce);
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Reward_Short")
        {
            if(Head.transform.position.y >= 1.65f)
            {
                AddReward(-1f);
            }

            else
            {
                AddReward(1f);
            }
        }

        else if(other.tag == "Reward_Tall")
        {
            if(Head.transform.position.y >= 1.65f)
            {
                AddReward(1f);
            }

            else
            {
                AddReward(-1f);
            }
        }
    }
}
