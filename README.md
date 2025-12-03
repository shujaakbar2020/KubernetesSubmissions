# KubernetesSubmissions

## Exercises

### Chapter 2

- [1.1.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.1/log_output)
- [1.2.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.2/the_project)
- [1.3.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.3/log_output)
- [1.4.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.4/the_project)
- [1.5.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.5/the_project)
- [1.6.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.6/the_project)
- [1.7.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.7/log_output)
- [1.8.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.8/the_project)
- [1.9.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.9/ping_pong)
- [1.10.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.10/log_output)
- [1.11.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.11)
- [1.12.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.12/the_project)
- [1.13.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/1.13/the_project)

### Chapter 3

- [2.1.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.1)
- [2.2.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.2/the_project)
- [2.3.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.3/log_output)
- [2.4.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.4/the_project)
- [2.5.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.5/log_output)
- [2.6.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.6)
- [2.7.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.7/ping_pong)
- [2.8.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.8/ping_pong)
- [2.9.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.9/the_project)
- [2.10.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/2.10/the_project)


### Chapter 4

- [3.1.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.1/ping_pong)
- [3.2.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.2/log_output)
- [3.3.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.3/log_output)
- [3.4.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.4/log_output)
- [3.5.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.5/the_project)
- [3.6.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.6/the_project)
- [3.7.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.7/the_project)
- [3.8.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.8/the_project)
- [3.9.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.9)
- [3.10.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.10/the_project)
- [3.11.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.11/the_project)
- [3.12.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/3.12/the_project)

### Chapter 5

- [4.1.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.1/)
- [4.2.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.2/the_project)
- [4.3.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.3/)
- [4.4.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.4/ping_pong)
- [4.5.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.5/the_project)
- [4.6.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.6/the_project)
- [4.7.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.7/log_output)
- [4.8.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.8/the_project)
- [4.9.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/4.9/the_project)
- [4.10.](https://github.com/shujaakbar2020/the_project_configs/tree/4.10)

### Chapter 6

- [5.1.](https://github.com/shujaakbar2020/KubernetesSubmissions/tree/5.1/crd)

# Database Choice on GKE

If we needs to deploy production applications on GKE, especially when reliability and low operational overhead are priorities, **Google Cloud SQL** is the preferred option.

## When to Choose Postgres on GKE with PVCs

We should consider running Postgres on GKE using PersistentVolumeClaims (PVCs) only if:

* We need full control over Postgres internals.
* We want to avoid Cloud SQL cost tiers.
* We are experienced with running databases in Kubernetes.
* We are prepared to manage backups, high availability (HA), replication, and updates manually.

## Recommendation

If high availability, automated backups, and minimized maintenance effort are priorities, **Cloud SQL** provides the safest and fastest path to production.
